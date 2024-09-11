from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category, Note
from .forms import TransactionForm, CategoryForm, NoteForm


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
    return render(request, 'transactions/home.html')


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