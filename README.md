# परम्परियम 

The official repository for परम्परियम cryptocurrency and file sharing system. Course project of EE706

# Core Functionalities

# Account

* (2048 bit) RSA public and private key

# Block

- timestamp
    - 64 bit unix timestamp
- nonce
    - 256 bit nonce
- file_hash
    - 256 bit
- transaction_hash
    - 256 bit
- prev_block_hash
    - 256 bit
- transaction_summary_block_hash
    - 256 bit
- data
    - 1024 bit
- difficulty
    - 8 bit (0 - 255) integer
- number
    - sequence number not included in calculation of hash

## Functions

* `mine_block`
* `verify_block`
* ``

# Transaction

- type
    - Coin transaction
    - File transaction
- Account from
    - The 2048 bit account address
- Accounts to
    - For coin transactions, all the accounts number appended back to back. A set of tuples (Account no, amount)
    - For file transaction, same as the "Account from" address. Set of tuple (Account from, file hash) 
- signature
    - 256 bit
    - private_key[SHA256(transaction)]

## Functions

* `new_transaction`
* `verify_transaction`

# Transaction Summary Block

> For coin transactions only

* signatures of transactions included as a list
* Input Accounts 
  * (Account number, amount)

* Output Accounts
  * (Account number, amount)