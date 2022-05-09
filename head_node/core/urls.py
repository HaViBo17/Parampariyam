from django.shortcuts import render
from . import views
from django.urls import path

urlpatterns =[
    path('',views.test),
    path('transaction_create/',views.transaction_create, name='new_transaction'),
    path('mine_block/',views.mine_block),
    path('share_transactions/',views.share_transactions),
    path('get_transactions/',views.get_transactions),
    path('get_blocks/',views.get_blocks),
    path('share_blocks/',views.share_blocks),
    path('blocks/',views.blocks),
]

