COIN_TRANSACTION = 1
FILE_TRANSACTION = 2

class Block:
    def __init__(self,params,difficulty,number):
        self.timestamp = params['timestamp']
        self.nonce = params['nonce']
        self.file_hash = params['file_hash']
        self.transaction_hash = params['transaction_hash']
        self.prev_block_hash = params['prev_block_hash']
        self.transaction_summary_hash = params['transaction_summary_hash']
        self.data = params['data']
        self.difficulty = difficulty
        self.number = number
    
    def __str__(self):
        return f"Number: {self.number} \nTimestamp: {self.timestamp}"

class Account:
    def __init__(self,address,balance):
        self.address = address
        self.balance = balance
    
        
class Transaction:
    def __init__(self,params):
        self.type = params['type']
        self.account_from = params['account_from']
        self.accounts_to = params['accounts_to'] ## list storing tuples (account,money)
        self.signature = params['signature']
        self.file_hash = params['file_hash']
    
class TransactionSummaryBlock:
    def __init__(self,params):
        self.type = params['type']
        self.acccounts_from = params['accounts_from']
        self.accounts_to = params['accounts_to']



