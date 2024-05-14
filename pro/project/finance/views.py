from django.shortcuts import render, redirect
from .models import Transaction, IncomeCategory, ExpenseCategory, Account
from decimal import Decimal
from django.db import models
from django.db.models import Q
from datetime import datetime

def home(request):
    income_categories = IncomeCategory.objects.all()
    expense_categories = ExpenseCategory.objects.all()
    account = Account.objects.first()
    total_income = Transaction.objects.filter(transaction_type='income').aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
    total_expense = Transaction.objects.filter(transaction_type='expense').aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')

    return render(request, 'home.html', {'income_categories': income_categories, 'expense_categories': expense_categories, 'account': account, 'total_income': total_income,
        'total_expense': total_expense})


def add_income(request):
    income_categories = IncomeCategory.objects.all()
    expense_categories = ExpenseCategory.objects.all()
    account = Account.objects.first()
    total_income = Transaction.objects.filter(transaction_type='income').aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
    total_expense = Transaction.objects.filter(transaction_type='expense').aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')

    

    if request.method == 'POST':
        date = request.POST.get('date_income')
        amount = Decimal(request.POST.get('amount_income', '0'))  # Set default value if empty
        category_id = request.POST.get('category_income')
        description = request.POST.get('description_income')

        if category_id:
            category = IncomeCategory.objects.get(id=category_id)
            Transaction.objects.create(
                date=date,
                amount=amount,
                category=category,
                description=description,
                transaction_type='income'
            )

            # Update account balance for income transaction
            account = Account.objects.first()  # Assuming there's only one account
            account.balance += amount
            account.save()

            return redirect('add_income')

    return render(request, 'home.html', {'income_categories': income_categories, 'expense_categories': expense_categories, 'account': account, 'total_income': total_income,
        'total_expense': total_expense})



def add_expense(request):
    income_categories = IncomeCategory.objects.all()
    expense_categories = ExpenseCategory.objects.all()
    account = Account.objects.first()
    total_income = Transaction.objects.filter(transaction_type='income').aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
    total_expense = Transaction.objects.filter(transaction_type='expense').aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')


    if request.method == 'POST':
        date = request.POST.get('date_expense')
        amount = Decimal(request.POST.get('amount_expense', '0'))  # Set default value if empty
        category_id = request.POST.get('category_expense')
        description = request.POST.get('description_expense')

        if category_id:
            category = ExpenseCategory.objects.get(id=category_id)
            Transaction.objects.create(
                date=date,
                amount=amount,
                category=category,
                description=description,
                transaction_type='expense'  # Set transaction_type to 'expense'
            )

            # Update account balance for expense transaction
            account = Account.objects.first()  # Assuming there's only one account
            account.balance -= amount
            account.save()

            return redirect('add_expense')

    return render(request, 'home.html',{'income_categories': income_categories, 'expense_categories': expense_categories, 'account': account, 'total_income': total_income,
        'total_expense': total_expense})


def hist_trans(request):
    # Get all transactions
    transactions = Transaction.objects.all()

    # Filter transactions based on the form submission
    if request.method == 'POST':
        filter_type = request.POST.get('filter_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Apply filtering based on the selected options
        if filter_type == 'income':
            transactions = transactions.filter(transaction_type='income')
        elif filter_type == 'expense':
            transactions = transactions.filter(transaction_type='expense')

        if start_date and end_date:
            # Convert dates from string to datetime objects
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            # Filter transactions within the specified date range
            transactions = transactions.filter(date__range=[start_date, end_date])

    # Get account balance
    account = Account.objects.first()

    # Sort transactions by date in descending order
    transactions = transactions.order_by('-date')

    # Render the template with the transactions and account balance
    return render(request, 'transactions.html', {'transactions': transactions, 'account': account})




from django.shortcuts import render, redirect
from .models import Transaction, ExpenseCategory, Account
from decimal import Decimal

def delete_transaction(request, transaction_id):
    if request.method == 'POST':
        transaction = Transaction.objects.get(id=transaction_id)
        is_income = (transaction.transaction_type == 'income')
        amount = transaction.amount

        account = Account.objects.first()
        if is_income:
            account.balance -= amount
        else:
            account.balance += amount

        account.save()

        if not is_income:
            category = transaction.category
            if isinstance(category, ExpenseCategory):  # Check if the category is an instance of ExpenseCategory
                category.total_expense -= amount
                category.save()

        transaction.delete()

        return redirect('hist_trans')

    return redirect('hist_trans')

def category_expenses(request):
    # Retrieve all expense categories and calculate total expenses for each category
    category_expenses = (
        ExpenseCategory.objects
        .annotate(total_expense=models.Sum('transaction__amount', filter=models.Q(transaction__transaction_type='expense')))
        .order_by('-total_expense')  # Sort categories by total_expense in descending order
    )

    return render(request, 'category.html', {
        'category_expenses': category_expenses
    })