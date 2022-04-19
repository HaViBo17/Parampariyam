from django.contrib import admin
from .models import *
# Register your models here.
admin.sites.register(Block)
admin.sites.register(Transaction)
admin.sites.register(TransactionSummaryBlock)