from django.urls import path
from .views import add_income, add_expense, hist_trans, home,delete_transaction,category_expenses
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', home, name='home'),  # Map root URL to the home view
    path('addincome/', add_income, name='add_income'),
    path('addexpense/', add_expense, name='add_expense'),
    path('hist_trans/', hist_trans, name='hist_trans'),

    path('category/',category_expenses , name='category_expenses'),
    path('delete/<int:transaction_id>/', delete_transaction, name='delete_transaction'),
    # Other URL patterns...
]
