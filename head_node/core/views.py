from wsgiref.util import request_uri
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import *
import json
from .methods import *
from .models import *
from headnode.settings import CERTIFICATE
# Create your views here.
def test(request):
    context = {
            'form':newTransactionForm(),
            'transactions' : ATransaction.objects.all(),
            'balance' : find_account_balance()
        }
    return render(request,'main.html', context )

def transaction_create(request):
    if request.method == 'POST':
        form = newTransactionForm(request.POST)
        if form.is_valid():
            #transaction_type = form.cleaned_data['type']
            #print(transaction_type)
            single_transaction(form.cleaned_data)
            p
            #print(transaction_type)

            # except:
            #     return HttpResponse('invalid accounts_to')
            return HttpResponse('Transaction created')
        
    return HttpResponse('transaction create view')

def mine_block(request):
    from .models import TransactionSummaryBlock, Block
    transaction_summary_block = createTransactionSummaryBlock()
    transactionSummaryHash = transaction_summary_block.get_hash()
    file_transaction_hash = transaction_summary_block.get_file_transaction_hash()
    coin_transaction_hash = transaction_summary_block.get_coin_transaction_hash()
    block_number = Block.objects.all().count()
    previous_block_hash = ""
    if block_number != 0:
        previous_block = Block.objects.get(number = block_number)
        previous_block_hash = previous_block.get_hash()
    data = ""
    difficulty = 5
    block = createBlock(file_transaction_hash,coin_transaction_hash,previous_block_hash,transactionSummaryHash,data,difficulty)
    test= mine(block,difficulty)
    print("heerere")
    print(test.get_hash())


    return HttpResponse('mine block view')

# to share the transactions with other nodes
def share_transactions(request):
    if request.method != 'GET':
        return HttpResponse('failure')
    data = []
    for transaction in ATransaction.objects.all().order_by('signature'):
        data.append(transaction.export_data())
    data = json.dumps(data)
    return_data = {
        'transactions': data,
        'signature': signer(data)
    }
    return JsonResponse(return_data)

# to get the transactions from other nodes
def get_transactions(request):
    peerNode = get_alive_node()
    url = peerNode.ip_address + ':' + peerNode.port
    r = requests.get(url + '/share_transactions')
    data = r.json()
    transactions = data['transactions']
    signature = data['signature']
    if verify(transactions, signature,peerNode.public_key):
        all_transactions = json.loads(transactions)
        for transaction in all_transactions:
            if ATransaction.objects.filter(signature=transaction['signature']).exists():
                continue
            new_transaction = ATransaction(
                type=transaction["type"],
                account_from=transaction["account_from"],
                accounts_to=transactions["accounts_to"],
                signature=signature,
                status = transaction["status"]
            )
    return HttpResponse('get transactions view')

def alive(request):
    return JsonResponse({
        'status' : 'alive'
    })

def share_blocks(request):
    if request.method != 'GET':
        return HttpResponse('failure')
    data = []
    for someBlock in Block.objects.all().order_by('number'):
        data.append(export_block(someBlock))
    data = json.dumps(data)
    return_data = {
        'blocks': data,
        'signature': signer(data)
    }
    return JsonResponse(return_data)


def get_blocks(request):
    peerNode = get_alive_node()
    url = peerNode.ip_address + ':' + peerNode.port
    r = requests.get(url + '/share_blocks')
    data = r.json()
    blocks = data['blocks']
    signature = data['signature']
    if verify(blocks, signature, peerNode.public_key):
        all_blocks = json.loads(blocks)
        received_difficulty = 0
        for block in all_blocks:
            if verify_block(block):
                received_difficulty += block['difficulty']
            else:
                print("error in received blocks")
        current_difficulty = 0
        for block in Block.objects.all().order_by('number'):
            current_difficulty += block.difficulty
        if received_difficulty > current_difficulty:
            for block in Block.objects.all():
                block.delete()
            for block in all_blocks:
                new_block = Block(
                    file_hash = block['file_hash'],
                    transaction_hash = block['transaction_hash'],
                    prev_block_hash = block['prev_block_hash'],
                    transaction_summary_hash = block['transaction_summary_hash'],
                    data = block['data'],
                    difficulty = block['difficulty'],
                    timestamp = block['timestamp']
                )
                new_block.save()

def share_certificate(request):
    return JsonResponse(data=CERTIFICATE)

def blocks(request):
    data = []
    for block in Block.objects.all().order_by('number'):
        data.append(export_block(block))
    return render(request,'blocks.html',{'blocks':data,'balance':find_account_balance()})