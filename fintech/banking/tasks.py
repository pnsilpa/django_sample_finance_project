# banking/tasks.py
from celery import shared_task
from .models import Account

@shared_task
def add_balance(account_id, amount):
    try:
        account = Account.objects.get(id=account_id)
        account.balance += amount
        account.save()
        return f"New balance for {account.account_number}: {account.balance}"
    except Account.DoesNotExist:
        return "Account not found"

@shared_task
def subtract_balance(account_id, amount):
    try:
        account = Account.objects.get(id=account_id)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            return f"New balance for {account.account_number}: {account.balance}"
        else:
            return "Insufficient funds"
    except Account.DoesNotExist:
        return "Account not found"
