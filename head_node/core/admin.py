from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Block)
admin.site.register(ATransaction)
admin.site.register(TransactionSummaryBlock)