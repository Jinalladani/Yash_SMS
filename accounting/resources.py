from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import IncomeCategoryModel, ExpenseCategoryModel, MemberVenderDetailModel, SocietyMemberDetailsModel, IncomeExpenseLedgerModel
from django.contrib.auth import get_user_model
User = get_user_model()

class IncomeCategoryResource(resources.ModelResource):

    class Meta:
        model = IncomeCategoryModel
        exclude = ('id', 'created', 'modified', 'user')

class ExpenseCategoryResource(resources.ModelResource):
    class Meta:
        model = ExpenseCategoryModel
        exclude = ('id', 'created', 'modified', 'user')

class MemberVenderDetailResource(resources.ModelResource):
    class Meta:
        model = MemberVenderDetailModel
        exclude = ('id', 'created', 'modified', 'user')

class SocietyMemberDetailsResource(resources.ModelResource):
    class Meta:
        model = SocietyMemberDetailsModel
        exclude = ('id', 'created', 'modified', 'user')

class IncomeExpenseLedgerResource(resources.ModelResource):
    class Meta:
        model = IncomeExpenseLedgerModel
        exclude = ('id', 'file','created', 'modified', 'user', 'opening_balance_cash', 'closing_balance_cash', 'opening_balance_bank', 'closing_balance_bank')
