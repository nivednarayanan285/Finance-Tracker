from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Account)
admin.site.register(IncomeCategory)
admin.site.register(ExpenseCategory)