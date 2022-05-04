from django.db import models
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
import json
import base64
from .methods import *

# Create your models here.
class Block(models.Model):
    timestamp = models.IntegerField()
    nonce = models.IntegerField(default=0)
    file_hash = models.CharField(max_length=1000)                          # stored as hexadecimal string
    transaction_hash = models.CharField(max_length=1000)                   # stored as hexadecimal string
    prev_block_hash = models.CharField(max_length=1000)                    # stored as hexadecimal string   
    transaction_summary_hash = models.CharField(max_length=1000)           # stored as hexadecimal string
    data = models.CharField(max_length=10000)                               # 1024 bit data object stored as base64 encoded string object
    difficulty = models.IntegerField()
    number = models.IntegerField(default=0)
    status_choices = (
        ('P', 'Pending'),
        ('M', 'Mined'),
        ('C', 'Confirmed')
    )
    status = models.CharField(max_length=1,choices=status_choices,default='P')
    
    def __str__(self):
        return f"Number: {self.number} \nTimestamp: {self.timestamp}"

    def export_data(self):
        data = {
            'timestamp': self.timestamp,
            'file_hash': self.file_hash,
            'transaction_hash': self.transaction_hash,
            'prev_block_hash': self.prev_block_hash,
            'transaction_summary_hash': self.transaction_summary_hash,
            'data': self.data,
            'difficulty': self.difficulty,
        }
        return data
    
    def get_hash(self):
        hash_object =  SHA256.new()
        bytes_data =  (self.timestamp).to_bytes(8, byteorder='big') \
                    + (self.nonce).to_bytes(8, byteorder='big') \
                    + bytes.fromhex(self.file_hash) \
                    + bytes.fromhex(self.transaction_hash) \
                    + bytes.fromhex(self.prev_block_hash) \
                    + bytes.fromhex(self.transaction_summary_hash) \
                    + base64.b64decode(self.data) \
                    + (self.difficulty).to_bytes(1, byteorder='big') 
        hash_object.update(bytes_data)
        return hash_object.hexdigest()

class ATransaction(models.Model):
    types = (
        ('C' , 'COIN_TRANSACTION'),
        ('F' , 'FILE_TRANSACTION'),
    )
    status = (
        ('P' , 'PENDING'),
        ('A' , 'APPROVED'), 
    )
    type = models.CharField(max_length=1, choices=types)
    account_from = models.JSONField()
    accounts_to = models.JSONField()
    signature = models.CharField(max_length=1000)
    status = models.CharField(max_length=1, default='P', choices=status)

class TransactionSummaryBlock(models.Model):
    accounts_from = models.JSONField()
    accounts_to = models.JSONField()
    included_transactions = models.ManyToManyField(ATransaction)

    def get_hash(self):
        hash_object =  SHA256.new()
        from_dict = json.loads(self.accounts_from)
        to_dict = json.loads(self.accounts_to)
        #print(self.accounts_from)
        for key in from_dict:
            #print(type(from_dict))
            key_cleaned = key_cleaner(key)
            hash_object.update(base64.b64decode(key_cleaned))
            value = from_dict[key]
            hash_object.update((value).to_bytes(8, byteorder='big'))
        for key in to_dict:
            key_cleaned = key_cleaner(key)
            hash_object.update(base64.b64decode(key_cleaned))
            value = to_dict[key]
            hash_object.update((value).to_bytes(8, byteorder='big'))
        transaction_signatures = []

        for some_transaction in self.included_transactions.all():
            transaction_signatures.append(some_transaction.signature)
        transaction_signatures.sort()

        for some_signature in transaction_signatures:
            hash_object.update(base64.b64decode(some_signature))
        return hash_object.hexdigest()
    
    def get_coin_transaction_hash(self):
        hash_object =  SHA256.new()
        for someTransaction in self.included_transactions.filter(type='C').order_by('signature'):
            hash_object.update(base64.b64decode(someTransaction.signature))
        return hash_object.hexdigest()
    
    def get_file_transaction_hash(self):
        hash_object =  SHA256.new()
        for someTransaction in self.included_transactions.filter(type='F').order_by('signature'):
            hash_object.update(base64.b64decode(someTransaction.signature))
        return hash_object.hexdigest()

class TransactionLinkNode(models.Model):
    transaction = models.ForeignKey(ATransaction, on_delete=models.PROTECT)
    next = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None)