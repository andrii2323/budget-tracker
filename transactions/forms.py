from django import forms
from .models import Transaction, Category, Note


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'category', 'description', 'transaction_type']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']