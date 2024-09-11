from django.db import models
from django.conf import settings


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,null=True, blank=True)
    description = models.TextField(blank=True)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)

    def __str__(self):
        return f"{self.amount} - {self.transaction_type} - {self.date}"


class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name


class Note(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='note')
    text = models.TextField()

    def __str__(self):
        return f"Note for transaction {self.transaction.id}"
