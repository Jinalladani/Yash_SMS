from django.contrib import admin
from accounting.models import ExpenseCategoryModel, \
    IncomeCategoryModel,BalanceModel,MemberVenderDetailModel,SocietyMemberDetailsModel, IncomeExpenseLedgerModel, LedgerFile
# Register your models here.

admin.site.register(ExpenseCategoryModel)
admin.site.register(IncomeCategoryModel)
admin.site.register(BalanceModel)
admin.site.register(MemberVenderDetailModel)
admin.site.register(SocietyMemberDetailsModel)
admin.site.register(IncomeExpenseLedgerModel)
admin.site.register(LedgerFile)
