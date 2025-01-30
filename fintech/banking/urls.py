# banking/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create_account/', views.create_account, name='create_account'),
    path('make_transaction/', views.make_transaction, name='make_transaction'),
    path('get_balance/<str:account_number>/', views.get_account_balance, name='get_account_balance'),
    path('get_transactions/<str:account_number>/', views.get_transactions, name='get_transactions'),
]
