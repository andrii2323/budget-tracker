from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.db.models import Sum
from django.db import models
from .models import Transaction, Category, Note
from .forms import TransactionForm, CategoryForm, NoteForm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')

    else:
        form = TransactionForm()
    return render(request, 'transactions/add_transaction.html', {'form': form})


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'transactions/transaction_list.html',
                  {'transactions': transactions})


@login_required
def add_note_to_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.transaction = transaction
            note.save()
            return redirect('transaction_list')
    else:
        form = NoteForm()
    return render(request, 'transactions/add_note.html',
                  {'form': form, 'transaction': transaction})


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'transactions/add_category.html',
                  {'form': form})


@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'transactions/category_list.html',
                  {'categories': categories})


def home(request):
    user = request.user
    total_income = Transaction.objects.filter(user=user, transaction_type='income').aggregate(total=models.Sum('amount'))['total'] or 0
    total_expense = Transaction.objects.filter(user=user, transaction_type='expense').aggregate(total=models.Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    context = {
        'balance': balance
    }
    return render(request, 'transactions/home.html', context)


@login_required
def add_income(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.transaction_type = 'income'
            transaction.user = request.user
            transaction.save()
            return redirect('home')
    else:
        form = TransactionForm()
    return render(request, 'transactions/add_transaction.html',
                  {'form': form, 'type': 'Income'})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.transaction_type = 'expense'
            transaction.user = request.user
            transaction.save()
            return redirect('home')
    else:
        form = TransactionForm()
    return render(request, 'transactions/add_transaction.html',
                  {'form': form, 'type': 'Expense'})


@login_required
def stats_view(request):
    user = request.user
    today = now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    year_ago = today - timedelta(days=365)

    transactions_week = Transaction.objects.filter(user=user, date__gte=week_ago)
    transactions_month = Transaction.objects.filter(user=user, date__gte=month_ago)
    transactions_year = Transaction.objects.filter(user=user, date__gte=year_ago)

    total_income_week = transactions_week.filter(transaction_type='income').aggregate(total=Sum('amount'))[
                             'total'] or 0
    total_expense_week = transactions_week.filter(transaction_type='expense').aggregate(total=Sum('amount'))[
                             'total'] or 0

    total_income_month = transactions_month.filter(transaction_type='income').aggregate(total=Sum('amount'))[
                             'total'] or 0
    total_expense_month = transactions_month.filter(transaction_type='expense').aggregate(total=Sum('amount'))[
                             'total'] or 0

    total_income_year = transactions_year.filter(transaction_type='income').aggregate(total=Sum('amount'))[
                             'total'] or 0
    total_expense_year = transactions_year.filter(transaction_type='expense').aggregate(total=Sum('amount'))[
                             'total'] or 0

    context = {
        'total_income_week': total_income_week,
        'total_expense_week': total_expense_week,
        'total_income_month': total_income_month,
        'total_expense_month': total_expense_month,
        'total_income_year': total_income_year,
        'total_expense_year': total_expense_year,
    }

    return render(request, 'transactions/stats.html', context)


@login_required
def category_pie_chart(request):
    user = request.user
    categories = Category.objects.filter(user=user)
    category_names = []
    category_totals = []

    for category in categories:
        total_expense = Transaction.objects.filter(user=user, category=category, transaction_type='expense').aggregate(
            total=Sum('amount'))['total'] or 0
        if total_expense > 0:
            category_names.append(category.name)
            category_totals.append(total_expense)

    plt.figure(figsize=(6, 6))
    plt.pie(category_totals, labels=category_names, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'transactions/category_pie_chart.html', {'graphic': graphic})


@login_required
def compare_periods(request):
    user = request.user
    today = now().date()
    current_month = today.month
    previous_month = (today - timedelta(days=30)).month

    transactions_current_month = Transaction.objects.filter(user=user, date__month=current_month)
    transactions_previous_month = Transaction.objects.filter(user=user, date__month=previous_month)

    income_current_month = transactions_current_month.filter(transaction_type='income').aggregate(total=Sum('amount'))[
                               'total'] or 0
    expense_current_month = transactions_current_month.filter(transaction_type='expense').aggregate(total=Sum('amount')
                                )['total'] or 0

    income_previous_month = transactions_previous_month.filter(transaction_type='income').aggregate(total=Sum('amount')
                                )['total'] or 0
    expense_previous_month = transactions_previous_month.filter(transaction_type='expense').aggregate(total=Sum('amount'
                                ))['total'] or 0

    context = {
        'income_current_month': income_current_month,
        'expense_current_month': expense_current_month,
        'income_previous_month': income_previous_month,
        'expense_previous_month': expense_previous_month,
    }

    return render(request, 'transactions/compare_periods.html', context)

