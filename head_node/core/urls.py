from django.shortcuts import render
from . import views
from django.urls import path

urlpatterns =[
    path('',views.test),
    path('transaction_create/',views.transaction_create, name='new_transaction'),
    path('mine_block/',views.mine_block),

]

