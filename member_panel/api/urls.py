from django.urls import path
from member_panel.api import views

urlpatterns = [
    path('list-member-income-expense-ledger/', views.MemberIncomeExpenseLedgerListJSONView.as_view(), name='list-member-income-expense-ledger'),
]
