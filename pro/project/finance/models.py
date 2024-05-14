from django.db import models

class Account(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Account Balance: ${self.balance}"



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class IncomeCategory(Category):
    class Meta:
        verbose_name_plural = "Income Categories"

    transaction_type = models.CharField(max_length=10, default='income')

class ExpenseCategory(Category):
    class Meta:
        verbose_name_plural = "Expense Categories"

    transaction_type = models.CharField(max_length=10, default='expense')



class Transaction(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    transaction_type = models.CharField(max_length=10, choices=[('income', 'Income'), ('expense', 'Expense')], default='income')  # Default value added

    def __str__(self):
        return f"{self.date} - {self.amount} - {self.category}"
