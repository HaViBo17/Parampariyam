from .models import * 
from django.conf import settings
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
import json
import base64
from Cryptodome.Hash import SHA256


def new_transaction(type,account_from, account_to):
    hash_object = SHA256.new()
    hash_object.update((type).encode('utf-8'))
    for key,value in account_from:
        hash_object.update(base64.b64decode(key))
        hash_object.update((value).to_bytes(8, byteorder='big'))
    for key,value in account_to:
        hash_object.update(base64.b64decode(key))
        hash_object.update((value).to_bytes(8, byteorder='big'))
    privatekey = RSA.importKey(settings.privatekey)
    signature = pkcs1_15.new(privatekey).sign(hash_object).hex()
    transaction = Transaction(type=type,account_from=account_from,accounts_to=account_to,signature=signature)
    transaction.save()

def get_hash(block):
    hash_object =  SHA256.new()
    bytes_data =  (block.timestamp).to_bytes(8, byteorder='big') \
                + (block.nonce).to_bytes(8, byteorder='big') \
                + bytes.fromhex(block.file_hash) \
                + bytes.fromhex(block.transaction_hash) \
                + bytes.fromhex(block.prev_block_hash) \
                + bytes.fromhex(block.transaction_summary_hash) \
                + base64.b64decode(block.data) \
                + (block.difficulty).to_bytes(1, byteorder='big') 
    hash_object.update(bytes_data)
    return hash_object.hexdigest()

def get_zeros(hash):
    count = 0
    for i in range(len(hash)):
        if hash[i] == '0':
            count += 4
        elif hash[i] ==  '1':
            count += 3
            return count
        elif hash[i] in '23':
            count += 2
            return count
        elif hash[i] in '4567':
            count += 1
            return count
        else:
            return count
    return count

def mine(block, difficulty):
    for i in range(2**256):
        block.nonce = i 
        block_hash = get_hash(block)
        if get_zeros(block_hash) >= difficulty:
            return block
    return None
        