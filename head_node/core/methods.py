
from django.conf import settings
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
import json
import base64
from Cryptodome.Hash import SHA256
import time


def key_cleaner(key):
    return key.replace("\n","").replace("\r","").replace("\t","").replace(" ","")


def make_pem(key,type):
    if type == 'public':
        return "-----BEGIN PUBLIC KEY-----\n" + key_cleaner(key) + "\n-----END PUBLIC KEY-----"
    elif type == 'private':
        return "-----BEGIN RSA PRIVATE KEY-----\n" + key_cleaner(key) + "\n-----END RSA PRIVATE KEY-----"

def remove_pem(key,type):
    if type == 'public':
        return key_cleaner(key.replace("-----BEGIN PUBLIC KEY-----\n","").replace("-----END PUBLIC KEY-----",""))
    elif type == 'private':
        return key_cleaner(key.replace("-----BEGIN RSA PRIVATE KEY-----\n","").replace("-----END RSA PRIVATE KEY-----",""))

def new_transaction(transaction_type, account_to):
    if 1:
        print("Start")
        hash_object = SHA256.new()
        print(transaction_type)
        hash_object.update(bytes(transaction_type, 'utf-8'))
       
        total_amount = 0
        # print(account_to)
        for key in account_to:
            key_cleaned = key_cleaner(key)
            hash_object.update(base64.b64decode(key_cleaned))
            value = account_to[key]
            hash_object.update((value).to_bytes(8, byteorder='big'))
            total_amount += value
        print(total_amount)
        
        account_from= {
            remove_pem(settings.PUBLIC_KEY,'public'): total_amount
        }

        hash_object.update(bytes(settings.PUBLIC_KEY2, 'utf-8'))
        hash_object.update((total_amount).to_bytes(8, byteorder='big'))


        privatekey = RSA.importKey(settings.PRIVATE_KEY)
        signature = pkcs1_15.new(privatekey).sign(hash_object).hex()

        # Do not store in PEM format
        accounts = {}
        for key in account_to:
            key_cleaned = key_cleaner(key)
            accounts[key_cleaned] = account_to[key]
        from .models import ATransaction
        thetransaction = ATransaction(type=transaction_type,account_from=account_from,accounts_to=accounts,signature=signature)
        thetransaction.save()
        return True
    # except:
    #     return False

def get_hash_block(block):
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
        block_hash = get_hash_block(block)
        if get_zeros(block_hash) >= difficulty:
            block.save()
            return block
    return None

def createTransactionSummaryBlock():
    from .models import ATransaction, TransactionSummaryBlock
    pendingTransactions = ATransaction.objects.filter(status='P').order_by('signature')
    to_dict = {}
    from_dict = {}
    for someTransaction in pendingTransactions:
        if someTransaction.type == 'F':
            continue
        accounts_to = someTransaction.accounts_to
        accounts_from = someTransaction.account_from
        for key in accounts_from:
            if key in from_dict:
                from_dict[key] += accounts_from[key]
            else:
                from_dict[key] = accounts_from[key]
        
        for key in accounts_to:
            if key in to_dict:
                to_dict[key] += accounts_to[key]
            else:
                to_dict[key] = accounts_to[key]
    transaction_summary = TransactionSummaryBlock(accounts_to=json.dumps(to_dict),accounts_from=json.dumps(from_dict))
    transaction_summary.save()
    for someTransaction in pendingTransactions:
        transaction_summary.included_transactions.add(someTransaction)
    transaction_summary.save()
    return transaction_summary



def createBlock(file_hash,transaction_hash,prev_block_hash,transaction_summary_hash,data,difficulty):
    from .models import Block
    timestamp = int(time.time())
    block = Block(
        timestamp=timestamp,
        file_hash=file_hash,
        transaction_hash=transaction_hash,
        prev_block_hash=prev_block_hash,
        transaction_summary_hash=transaction_summary_hash,
        data=data,
        difficulty=difficulty)
    block.save()
    return block

        