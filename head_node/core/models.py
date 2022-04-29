from django.db import models
from Cryptodome.Hash import SHA256
import base64

# Create your models here.
class Block(models.Model):
    timestamp = models.IntegerField()
    nonce = models.IntegerField()
    file_hash = models.CharField()                          # stored as hexadecimal string
    transaction_hash = models.CharField()                   # stored as hexadecimal string
    prev_block_hash = models.CharField()                    # stored as hexadecimal string   
    transaction_summary_hash = models.CharField()           # stored as hexadecimal string
    data = models.TextField()                               # 1024 bit data object stored as base64 encoded string object
    difficulty = models.IntegerField()
    number = models.IntegerField()
    
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

class Transaction(models.Model):
    types = (
        ('C' , 'COIN_TRANSACTION'),
        ('F' , 'FILE_TRANSACTION'),
    )
    type = models.CharField(max_length=1, choices=types)
    account_from = models.JSONField()
    accounts_to = models.JSONField()
    signature = models.CharField()

class TransactionSummaryBlock(models.Model):
    types = (
        ('C' , 'COIN_TRANSACTION'),
        ('F' , 'FILE_TRANSACTION'),
    )
    type = models.CharField(max_length=1, choices=types)
    accounts_from = models.JSONField()
    accounts_to = models.JSONField()
    
