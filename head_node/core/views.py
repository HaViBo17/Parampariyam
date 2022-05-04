from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
import json
from .methods import *
from .models import *
# Create your views here.
def test(request):
    return render(request,'main.html', {'form':newTransactionForm()})

def transaction_create(request):
    if request.method == 'POST':
        form = newTransactionForm(request.POST)
        if form.is_valid():
            transaction_type = form.cleaned_data['type']
            print(transaction_type)
            accounts_to = form.cleaned_data['accounts_to']
            
            accounts = json.loads(accounts_to)
            new_transaction(transaction_type, accounts)
            print(transaction_type)

            # except:
            #     return HttpResponse('invalid accounts_to')
            return HttpResponse('Transaction created')
        
    return HttpResponse('transaction create view')

def mine_block(request):
    from .models import TransactionSummaryBlock
    transaction_summary_block = createTransactionSummaryBlock()
    transactionSummaryHash = transaction_summary_block.get_hash()
    file_transaction_hash = transaction_summary_block.get_file_transaction_hash()
    coin_transaction_hash = transaction_summary_block.get_coin_transaction_hash()
    previous_block_hash = coin_transaction_hash
    data = ""
    difficulty = 5
    block = createBlock(file_transaction_hash,coin_transaction_hash,previous_block_hash,transactionSummaryHash,data,difficulty)
    test= mine(block,difficulty)
    print("heerere")
    print(test.get_hash())


    return HttpResponse('mine block view')
