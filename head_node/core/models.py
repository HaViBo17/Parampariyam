from ipaddress import ip_address
from django.db import models
from rsa import PublicKey
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
import json
import base64
from core.methods import key_cleaner, make_pem,remove_pem,key_bytes,signer_without_hash,signer,verify,export_block,single_transaction,new_transaction,get_hash_block,get_zeros,mine,createTransactionSummaryBlock,createBlock,get_alive_node,verify_block,find_account_balance

# for blockchain core
class Block(models.Model):
    timestamp = models.IntegerField()
    nonce = models.IntegerField(default=0)
    file_hash = models.CharField(max_length=1000)                          # stored as hexadecimal string
    transaction_hash = models.CharField(max_length=1000)                   # stored as hexadecimal string
    prev_block_hash = models.CharField(max_length=1000)                    # stored as hexadecimal string   
    transaction_summary_hash = models.CharField(max_length=1000)           # stored as hexadecimal string
    data = models.CharField(max_length=10000)                               # 1024 bit data object stored as base64 encoded string object
    difficulty = models.IntegerField()
    number = models.IntegerField(default=1)
    status_choices = (
        ('P', 'Pending'),
        ('M', 'Mined'),
        ('C', 'Confirmed')
    )
    status = models.CharField(max_length=1,choices=status_choices,default='P')
    block_number = models.IntegerField(default=0)
    transaction_summary_block = models.ForeignKey('TransactionSummaryBlock', on_delete=models.CASCADE, null=True)
    miner = models.CharField(max_length=1000,null=True,blank=True)
    
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
            'nonce': self.nonce,
            'number': self.number,
            'miner' : self.miner
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
                    + (self.difficulty).to_bytes(1, byteorder='big') \
                    + base64.b64decode(remove_pem(self.miner,'public')) 
        hash_object.update(bytes_data)
        return hash_object.hexdigest()

class ATransaction(models.Model):
    types = (
        ('C' , 'COIN_TRANSACTION'),
        ('F' , 'FILE_TRANSACTION'),
    )
    status_choices = (
        ('P' , 'PENDING'),
        ('A' , 'APPROVED'), 
    )
    transaction_type = models.CharField(max_length=1, choices=types)
    account_from = models.CharField(max_length=1000)
    account_to = models.CharField(max_length=1000)
    transaction_data = models.CharField(max_length=1000)
    transaction_fees = models.IntegerField()
    signature = models.CharField(max_length=1000)
    status = models.CharField(max_length=1, default='P', choices=status_choices)

    def export_data(self):
        data = {
            'transaction_type': self.transaction_type,
            'account_from': self.account_from,
            'account_to': self.account_to,
            'transaction_data' : self.transaction_data,
            'transaction_fees' : self.transaction_fees,
            'signature': self.signature,
            'status': self.status,
        }
        return data
    

class TransactionSummaryBlock(models.Model):
    accounts_from = models.JSONField()
    accounts_to = models.JSONField()
    included_transactions = models.ManyToManyField(ATransaction)

    def get_hash(self):
        return ""
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
        for someTransaction in ATransaction.objects.filter(transaction_type='C',status='P').order_by('signature'):
            return someTransaction.signature
        return ""
    
    def get_file_transaction_hash(self):
        for someTransaction in ATransaction.objects.filter(transaction_type='F',status='P').order_by('signature'):
            return someTransaction.signature
        return ""

class TransactionLinkNode(models.Model):
    transaction = models.ForeignKey(ATransaction, on_delete=models.PROTECT)
    next = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None)

# for peer networking
class Certificate(models.Model):
    subject_public_key = models.CharField(max_length=1000)
    issuer_public_key = models.CharField(max_length=1000)
    valid_till = models.IntegerField(default=0)
    valid_from = models.IntegerField(default=0)
    signature = models.CharField(max_length=1000)

    def export_data(self):
        data = {
            'subject_public_key': remove_pem(self.subject_public_key),
            'issuer_public_key': remove_pem(self.issuer_public_key),
            'valid_till': self.valid_till,
            'valid_from': self.valid_from,
            'signature': self.signature,
        }
        return data

class Peer(models.Model):
    public_key = models.CharField(max_length=1000)
    certificate = models.ForeignKey(Certificate, on_delete=models.PROTECT)
    familiarity = models.IntegerField(default=0)
    ip_address = models.CharField(max_length=1000)
    port = models.IntegerField(default=0)

class AccountHolder(models.Model):
    public_key = models.CharField(max_length=1000)
    certificate = models.ForeignKey(Certificate, on_delete=models.PROTECT, null=True, blank=True)
    balance = models.IntegerField(default=0)


