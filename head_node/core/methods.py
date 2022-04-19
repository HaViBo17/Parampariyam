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
    signature = pkcs1_15.new(privatekey).sign(hash_object)
    transaction = Transaction(type=type,account_from=account_from,accounts_to=account_to,signature=signature)
    transaction.save()
