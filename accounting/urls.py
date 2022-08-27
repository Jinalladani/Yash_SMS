from django.urls import path
from accounting import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('income-category/', views.IncomeCategory.as_view(), name='income-category'),
    path('add-income-category/', views.IncomeCategoryCreateView.as_view(), name='add-income-category'),
    path('update-income-category/<int:pk>', views.IncomeCategoryUpdateView.as_view(), name='update-income-category'),
    path('export-income-category/', views.IncomeCategoryExportView.as_view(), name="export-income-category"),

    path('expense-category/', views.ExpenseCategory.as_view(), name='expense-category'),
    path('add-expense-category/', views.ExpenseCategoryCreateView.as_view(), name='add-expense-category'),
    path('update-expense-category/<int:pk>', views.ExpenseCategoryUpdateView.as_view(), name='update-expense-category'),
    path('export-expense-category/', views.ExpenseCategoryExportView.as_view(), name="export-expense-category"),

    path('members-vendor/', views.MembersVender.as_view(), name='members-vendor'),
    path('add-members-vendor/', views.MembersVenderCreateView.as_view(), name='add-members-vendor'),
    path('update-members-vendor/<int:pk>', views.MembersVenderUpdateView.as_view(), name='update-members-vendor'),
    path('export-members-vendor/', views.MembersVenderExportView.as_view(), name="export-members-vendor"),

    path('member-details/', views.MemberDetails.as_view(), name='member-details'),
    path('add-member-details/', views.MemberDetailsCreateView.as_view(), name='add-member-details'),
    path('update-member-details/<int:pk>', views.MemberDetailsUpdateView.as_view(), name='update-member-details'),
    path('export-member-details/', views.MemberDetailsExportView.as_view(), name="export-member-details"),

    path('balance/', views.Balance.as_view(), name='balance'),
    path('add-balance/', views.BalanceCreateView.as_view(), name='add-balance'),
    path('update-balance/<int:pk>', views.BalanceUpdateView.as_view(), name='update-balance'),

    path('income-expense-ledger/', views.IncomeExpenseLedger.as_view(), name='income-expense-ledger'),
    path('add-income-expense-ledger/', views.IncomeExpenseLedgerCreateView.as_view(), name='add-income-expense-ledger'),
    path('update-income-expense-ledger/<int:pk>', views.IncomeExpenseLedgerUpdateView.as_view(), name='update-income-expense-ledger'),
    path('export-income-expense-ledger/', views.IncomeExpenseLedgerExportView.as_view(), name="export-income-expense-ledger"),
    path('export-filtered-income-expense-ledger/', views.FilteredIncomeExpenseLedgerExportView.as_view(), name="export-filtered-income-expense-ledger"),
    path('upload-ledger-file/<int:pk>', views.UploadLedgerFileView.as_view(), name='upload-ledger-file'),

    path('upload-excel/', views.UploadExcel.as_view(), name='upload-excel'),
    path('cash-withdrawal/', views.CashWithdrawalView.as_view(), name='cash-withdrawal'),
    path('cash-deposit/', views.CashDepositView.as_view(), name='cash-deposit'),

]