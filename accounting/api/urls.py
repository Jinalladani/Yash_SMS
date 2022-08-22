from django.urls import path
from accounting.api import views

urlpatterns = [
    path('list-income-category/', views.IncomeCategoryRecordListJSON.as_view(), name='list-income-category'),
    path('list-expense-category/', views.ExpenseCategoryRecordListJSON.as_view(), name='list-expense-category'),
    path('list-members-vendor/', views.MembersVendorRecordListJSON.as_view(), name='list-members-vendor'),
    path('list-members-details/', views.MemberDetailsRecordListJSON.as_view(), name='list-members-details'),
    path('list-balance/', views.BalanceRecordListJSON.as_view(), name='list-balance'),
    path('list-income-expense-ledger/', views.IncomeExpenseLedgerListJSON.as_view(), name='list-income-expense-ledger'),

    path('upload-excel-api/', views.ImportExcelApiView.as_view(), name='upload-excel-api'),

    # delete url
    path('incomecategory/delete/<int:pk>/',  views.IncomeCategoryDeleteView.as_view(), name='incomecategory'),
    path('expensecategory/delete/<int:pk>/',  views.ExpenseCategoryDeleteView.as_view(), name='expensecategory'),
    path('membersvender/delete/<int:pk>/',  views.MembersVenderDeleteView.as_view(), name='membersvender'),
    path('memberdetails/delete/<int:pk>/',  views.MemberDetailsDeleteView.as_view(), name='memberdetails'),
    path('balance/delete/<int:pk>/',  views.BalanceDeleteView.as_view(), name='balance'),
    path('incomeexpenseledger/delete/<int:pk>/',  views.IncomeExpenseLedgerDeleteView.as_view(), name='incomeexpenseledger'),

    # bulk delete
    path('bulk-delete/',  views.BulkDeleteApiView.as_view(), name='bulk-delete'),
    path("get-category-header/", views.CategoryHeaderApiView.as_view(), name="get-category-header")

]