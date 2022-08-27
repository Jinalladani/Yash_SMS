from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from import_export import resources
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tablib import Dataset
from rest_framework.authentication import SessionAuthentication
import json
from datetime import datetime, timedelta

from accounting.models import BalanceModel, ExpenseCategoryModel, IncomeCategoryModel, MemberVenderDetailModel, SocietyMemberDetailsModel, IncomeExpenseLedgerModel

from accounting.resources import IncomeCategoryResource, ExpenseCategoryResource, MemberVenderDetailResource, SocietyMemberDetailsResource, User

class MemberIncomeExpenseLedgerListJSONView(BaseDatatableView):
    model = IncomeExpenseLedgerModel
    columns = [
        'id',
        'date',
        'type',
        'amount',
        'category_header',
        'from_or_to_account',
        'transaction_type',
        'transaction_details',
        'voucherNo_or_invoiceNo',
        'file',
        'remark',
        'opening_balance_cash',
        'closing_balance_cash',
        'opening_balance_bank',
        'closing_balance_bank',
    ]
    order_columns = [
        'id',
        'date',
        'type',
        'amount',
        'category_header',
        'from_or_to_account',
        'transaction_type',
        'transaction_details',
        'voucherNo_or_invoiceNo',
        'file',
        'remark',
        'opening_balance_cash',
        'closing_balance_cash',
        'opening_balance_bank',
        'closing_balance_bank',
    ]

    def render_column(self, row, column):
        if column == 'file':
            if len(row.LedgerFile.all()):
                return row.LedgerFile.all().first().file.url
            else:
                return False
        else:
            return super(MemberIncomeExpenseLedgerListJSONView, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(type__contains=search))
        if self.request.GET.get('columns[2][search][value]'):
            data = json.loads(self.request.GET.get('columns[2][search][value]'))
            for i in data:
                if i['name'] == "transaction_type":
                    qs = qs.filter(Q(transaction_type__contains=i['value']))
                if i['name'] == "category_header":
                    qs = qs.filter(Q(category_header__contains=i['value']))
                if i['name'] == "member":
                    qs = qs.filter(Q(from_or_to_account__contains=i['value']))
                if i['name'] == "type":
                    qs = qs.filter(Q(type__contains=i['value']))
                if i['name'] == "start":
                    if i['value']:
                        qs = qs.filter(Q(created__date__gte=datetime.strptime(i['value'], "%Y-%m-%d")))
                if i['name'] == "end":
                    if i['value']:
                        qs = qs.filter(Q(created__date__lte=datetime.strptime(i['value'], "%Y-%m-%d")))
        return qs
        

    def get_initial_queryset(self):
        pk = self.request.GET.get("society_id")
        return self.model.objects.filter(user= User.objects.get(pk= pk))
