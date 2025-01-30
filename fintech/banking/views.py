# banking/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
import json
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["POST"])
def create_account(request):
    data = json.loads(request.body)
    account_number = data.get('account_number')
    account_holder = data.get('account_holder')

    if not account_number or not account_holder:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    account = Account.objects.create(account_number=account_number, account_holder=account_holder)
    return JsonResponse({'message': 'Account created successfully', 'account_id': account.id})

# @csrf_exempt
# @require_http_methods(["POST"])
# def make_transaction(request):
#     data = json.loads(request.body)
#     account_id = data.get('account_id')
#     transaction_type = data.get('transaction_type')
#     amount = data.get('amount')
#
#     if not account_id or not transaction_type or not amount:
#         return JsonResponse({'error': 'Missing required fields'}, status=400)
#
#     try:
#         account = Account.objects.get(id=account_id)
#     except Account.DoesNotExist:
#         return JsonResponse({'error': 'Account not found'}, status=404)
#
#     if transaction_type == 'deposit':
#         account.balance += amount
#     elif transaction_type == 'withdrawal':
#         if account.balance >= amount:
#             account.balance -= amount
#         else:
#             return JsonResponse({'error': 'Insufficient funds'}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid transaction type'}, status=400)
#
#     account.save()
#     Transaction.objects.create(account=account, transaction_type=transaction_type, amount=amount)
#     return JsonResponse({'message': f'{transaction_type.capitalize()} successful', 'new_balance': account.balance})

from .tasks import add_balance, subtract_balance

@csrf_exempt
@require_http_methods(["POST"])
def make_transaction(request):
    data = json.loads(request.body)
    account_id = data.get('account_id')
    transaction_type = data.get('transaction_type')
    amount = data.get('amount')

    if not account_id or not transaction_type or not amount:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    if transaction_type == 'deposit':
        add_balance.delay(account_id, amount)
        return JsonResponse({'message': 'Deposit task added to queue'})
    elif transaction_type == 'withdrawal':
        subtract_balance.delay(account_id, amount)
        return JsonResponse({'message': 'Withdrawal task added to queue'})
    else:
        return JsonResponse({'error': 'Invalid transaction type'}, status=400)



@require_http_methods(["GET"])
def get_account_balance(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)

    return JsonResponse({'account_number': account.account_number, 'balance': str(account.balance)})

@require_http_methods(["GET"])
def get_transactions(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)

    transactions = account.transactions.all().values('transaction_type', 'amount', 'timestamp')
    return JsonResponse({'transactions': list(transactions)})

