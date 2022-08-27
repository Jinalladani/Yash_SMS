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

from accounting.resources import IncomeCategoryResource, ExpenseCategoryResource, MemberVenderDetailResource, SocietyMemberDetailsResource

class IncomeCategoryRecordListJSON(BaseDatatableView):
    model = IncomeCategoryModel
    columns = ['id', 'category']
    order_columns = ['id', 'category']

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(category__contains=search))
        return qs

    def get_initial_queryset(self):
        return self.model.objects.filter(user= self.request.user)

class ExpenseCategoryRecordListJSON(BaseDatatableView):
    model = ExpenseCategoryModel
    columns = ['id', 'category']
    order_columns = ['id', 'category']

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(category__contains=search))
        return qs

    def get_initial_queryset(self):
        return self.model.objects.filter(user= self.request.user)

class MembersVendorRecordListJSON(BaseDatatableView):
    model = MemberVenderDetailModel
    columns = ['id', 'name']
    order_columns = ['id', 'name']

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(name__contains=search))
        return qs

    def get_initial_queryset(self):
        return self.model.objects.filter(user= self.request.user)

class MemberDetailsRecordListJSON(BaseDatatableView):
    model = SocietyMemberDetailsModel
    columns = ["id", "flat_no","primary_name","primary_contact_no","secondary_name","secondary_contact_no","accounting_name","whatsapp_contact_no","email","residence"]
    order_columns = ["id", "flat_no","primary_name","primary_contact_no","secondary_name","secondary_contact_no","accounting_name","whatsapp_contact_no","email","residence"]

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(primary_name__contains=search))
        return qs

    def get_initial_queryset(self):
        return self.model.objects.filter(user= self.request.user)

class BalanceRecordListJSON(BaseDatatableView):
    model = BalanceModel
    columns = ["id", "account", "balance_amount"]
    order_columns = ["id", "account", "balance_amount"]

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(account__contains=search))
        return qs

    def get_initial_queryset(self):
        return self.model.objects.filter(user= self.request.user)

class IncomeExpenseLedgerListJSON(BaseDatatableView):
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
            return super(IncomeExpenseLedgerListJSON, self).render_column(row, column)

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
        return self.model.objects.filter(user= self.request.user)

# Importing the excel file
class ImportExcelApiView(APIView):

    def add_balance_cash(self, request, transaction_type, amount, income_or_expense):
        if(income_or_expense == "Income"):
            if transaction_type == "Cash":
                opening_balance_cash = BalanceModel.objects.filter(user= request.user, account="Cash").first().balance_amount
                balance_model_instance = BalanceModel.objects.filter(user= request.user, account="Cash").first()
                balance_model_instance.balance_amount += amount
                balance_model_instance.save()
                closing_balance_cash = balance_model_instance.balance_amount
                opening_balance_bank = BalanceModel.objects.filter(user= request.user, account="Bank").first().balance_amount
                closing_balance_bank = BalanceModel.objects.filter(user= request.user, account="Bank").first().balance_amount
                return opening_balance_cash, closing_balance_cash, opening_balance_bank, closing_balance_bank

            elif transaction_type == "Bank":
                opening_balance_bank = BalanceModel.objects.filter(user= request.user, account="Bank").first().balance_amount
                balance_model_instance = BalanceModel.objects.filter(user= request.user, account="Bank").first()
                balance_model_instance.balance_amount += amount
                balance_model_instance.save()
                closing_balance_bank = balance_model_instance.balance_amount
                opening_balance_cash = BalanceModel.objects.filter(user= request.user, account="Cash").first().balance_amount
                closing_balance_cash = BalanceModel.objects.filter(user= request.user, account="Cash").first().balance_amount
                return opening_balance_cash, closing_balance_cash, opening_balance_bank, closing_balance_bank

        elif(income_or_expense == "Expense"):
            if transaction_type == "Cash":
                opening_balance_cash = BalanceModel.objects.filter(user= request.user, account="Cash").first().balance_amount
                balance_model_instance = BalanceModel.objects.filter(user= request.user, account="Cash").first()
                balance_model_instance.balance_amount -= amount
                balance_model_instance.save()
                closing_balance_cash = balance_model_instance.balance_amount
                opening_balance_bank = BalanceModel.objects.filter(user= request.user, account="Bank").first().balance_amount
                closing_balance_bank = BalanceModel.objects.filter(user= request.user, account="Bank").first().balance_amount
                return opening_balance_cash, closing_balance_cash, opening_balance_bank, closing_balance_bank

            elif transaction_type == "Bank":
                opening_balance_bank = BalanceModel.objects.filter(user= request.user, account="Bank").first().balance_amount
                balance_model_instance = BalanceModel.objects.filter(user= request.user, account="Bank").first()
                balance_model_instance.balance_amount -= amount
                balance_model_instance.save()
                closing_balance_bank = balance_model_instance.balance_amount
                opening_balance_cash = BalanceModel.objects.filter(user= request.user, account="Cash").first().balance_amount
                closing_balance_cash = BalanceModel.objects.filter(user= request.user, account="Cash").first().balance_amount
                return opening_balance_cash, closing_balance_cash, opening_balance_bank, closing_balance_bank

        elif(income_or_expense == "CASH OUT"):
            bank = BalanceModel.objects.filter(user= request.user, account= "Bank").first()
            cash = BalanceModel.objects.filter(user= request.user, account= "Cash").first()

            opening_balance_cash = cash.balance_amount
            opening_balance_bank = bank.balance_amount

            bank.balance_amount = bank.balance_amount - amount
            bank.save()
            cash.balance_amount = cash.balance_amount + amount
            cash.save()

            closing_balance_cash = cash.balance_amount
            closing_balance_bank = bank.balance_amount
            return opening_balance_cash, closing_balance_cash, opening_balance_bank, closing_balance_bank

        elif(income_or_expense == "CASH IN"):
            bank = BalanceModel.objects.filter(user= request.user, account= "Bank").first()
            cash = BalanceModel.objects.filter(user= request.user, account= "Cash").first()

            opening_balance_cash = cash.balance_amount
            opening_balance_bank = bank.balance_amount

            bank.balance_amount = bank.balance_amount + amount
            bank.save()
            cash.balance_amount = cash.balance_amount - amount
            cash.save()

            closing_balance_cash = cash.balance_amount
            closing_balance_bank = bank.balance_amount
            return opening_balance_cash, closing_balance_cash, opening_balance_bank, closing_balance_bank
    
    def create_if_not_exist_category(self, category_type, ele):
        if category_type == "Income":
            obj, created = IncomeCategoryModel.objects.get_or_create(   user=  self.request.user,
                                                                        category= ele)
        elif category_type == "Expense":
            obj, created = ExpenseCategoryModel.objects.get_or_create(  user=  self.request.user,
                                                                        category= ele)

    def create_if_not_exist_member_vendor(self, ele):
        obj, created = MemberVenderDetailModel.objects.get_or_create(   user=  self.request.user,
                                                                        name= ele)

    def post(self, request):
        dataset = Dataset()
        for file in request.FILES:  
            if file == "uppy-income-category":
                data = request.FILES['uppy-income-category']
                imported_data = dataset.load(data.read())

                try:
                    for i in imported_data.dict:
                        IncomeCategoryModel.objects.create( category= i.get("category"),
                                                            user= request.user)
                except Exception as e:
                    print(e)

            if file == "uppy-expense-category":
                data = request.FILES['uppy-expense-category']
                imported_data = dataset.load(data.read())

                try:
                    for i in imported_data.dict:
                        ExpenseCategoryModel.objects.create(category= i.get("category"),
                                                            user= request.user)
                except Exception as e:
                    print(e)

            if file == "uppy-members-vendor-category":
                data = request.FILES['uppy-members-vendor-category']
                imported_data = dataset.load(data.read())

                try:
                    for i in imported_data.dict:
                        MemberVenderDetailModel.objects.create( name= i.get("name"),
                                                                user= request.user)
                except Exception as e:
                    print(e)

            if file == "uppy-members-category":
                data = request.FILES['uppy-members-category']
                imported_data = dataset.load(data.read())

                try:
                    for i in imported_data.dict:
                        SocietyMemberDetailsModel.objects.create(   flat_no= i.get("flat_no"),
                                                                    primary_name= i.get("primary_name"),
                                                                    primary_contact_no= i.get("primary_contact_no"),
                                                                    secondary_name= i.get("secondary_name"),
                                                                    secondary_contact_no= i.get("secondary_contact_no"),
                                                                    accounting_name= i.get("accounting_name"),
                                                                    whatsapp_contact_no= i.get("whatsapp_contact_no"),
                                                                    email= i.get("email"),
                                                                    residence= i.get("residence"),
                                                                    user= request.user)
                except Exception as e:
                    print(e)

            if file == "uppy-ledger-category":
                data = request.FILES['uppy-ledger-category']
                imported_data = dataset.load(data.read())

                try:
                    for i in imported_data.dict:
                        transaction_type = i.get("transaction_type")
                        amount = i.get("amount")
                        income_or_expense = i.get("type")
                        if transaction_type and amount and income_or_expense:
                            opening_balance_cash, closing_balance_cash, opening_balance_bank, closing_balance_bank = self.add_balance_cash(self.request, transaction_type, amount, income_or_expense)
                            self.create_if_not_exist_category(income_or_expense, i.get("category_header"))
                            self.create_if_not_exist_member_vendor(i.get("from_or_to_account"))
                            IncomeExpenseLedgerModel.objects.create(    user = request.user,
                                                                        date = i.get("date"),
                                                                        type = i.get("type"),
                                                                        amount = i.get("amount"),
                                                                        category_header = i.get("category_header"),
                                                                        from_or_to_account = i.get("from_or_to_account"),
                                                                        transaction_type = i.get("transaction_type"),
                                                                        transaction_details = i.get("transaction_details"),
                                                                        voucherNo_or_invoiceNo = i.get("voucherNo_or_invoiceNo"),
                                                                        remark = i.get("remark"),
                                                                        opening_balance_cash = opening_balance_cash,
                                                                        closing_balance_cash = closing_balance_cash,
                                                                        opening_balance_bank = opening_balance_bank,
                                                                        closing_balance_bank = closing_balance_bank
                            )
                        else:
                            raise Exception
                except Exception as e:
                    print(e)

        return Response({"status": True}, status=status.HTTP_200_OK)


# all Delete view
class IncomeCategoryDeleteView(APIView):
    authentication_classes = [SessionAuthentication]

    def delete(self, request, pk):
        object = IncomeCategoryModel.objects.get(pk=pk)
        object.delete()
        return Response({"message": "Data Deleted Successfully"})

class ExpenseCategoryDeleteView(APIView):
    authentication_classes = [SessionAuthentication]

    def delete(self, request, pk):
        object = ExpenseCategoryModel.objects.get(pk=pk)
        object.delete()
        return Response({"message": "Data Deleted Successfully"})

class MembersVenderDeleteView(APIView):
    authentication_classes = [SessionAuthentication]

    def delete(self, request, pk):
        object = MemberVenderDetailModel.objects.get(pk=pk)
        object.delete()
        return Response({"message": "Data Deleted Successfully"})

class MemberDetailsDeleteView(APIView):
    authentication_classes = [SessionAuthentication]

    def delete(self, request, pk):
        object = SocietyMemberDetailsModel.objects.get(pk=pk)
        object.delete()
        return Response({"message": "Data Deleted Successfully"})

class BalanceDeleteView(APIView):
    authentication_classes = [SessionAuthentication]

    def delete(self, request, pk):
        object = BalanceModel.objects.get(pk=pk)
        object.delete()
        return Response({"message": "Data Deleted Successfully"})

class IncomeExpenseLedgerDeleteView(APIView):
    authentication_classes = [SessionAuthentication]

    def delete(self, request, pk):
        object = IncomeExpenseLedgerModel.objects.get(pk=pk)
        object.delete()
        return Response({"message": "Data Deleted Successfully"})

# bulk delete
class BulkDeleteApiView(APIView):

    def delete(self, request):
        if request.data.get("model_name")  == "ExpenseCategoryModel":
            queryset = ExpenseCategoryModel.objects.filter(pk__in= request.data.getlist("pk_array[]"))
            queryset.delete()

        if request.data.get("model_name")  == "IncomeCategoryModel":
            queryset = IncomeCategoryModel.objects.filter(pk__in= request.data.getlist("pk_array[]"))
            queryset.delete()

        if request.data.get("model_name")  == "BalanceModel":
            queryset = BalanceModel.objects.filter(pk__in= request.data.getlist("pk_array[]"))
            queryset.delete()

        if request.data.get("model_name")  == "MemberVenderDetailModel":
            queryset = MemberVenderDetailModel.objects.filter(pk__in= request.data.getlist("pk_array[]"))
            queryset.delete()

        if request.data.get("model_name")  == "SocietyMemberDetailsModel":
            queryset = SocietyMemberDetailsModel.objects.filter(pk__in= request.data.getlist("pk_array[]"))
            queryset.delete()

        if request.data.get("model_name")  == "IncomeExpenseLedgerModel":
            queryset = IncomeExpenseLedgerModel.objects.filter(pk__in= request.data.getlist("pk_array[]"))
            queryset.delete()

        return Response({"message": "Data Deleted Successfully"})

class CategoryHeaderApiView(APIView):

    def get(self, request):
        transaction_type = request.query_params.get("type")

        if(transaction_type == "income"):
            return Response(IncomeCategoryModel.objects.filter(user= request.user).values("category"))
        elif(transaction_type == "expense"):
            return Response(ExpenseCategoryModel.objects.filter(user= request.user).values("category"))
        elif(transaction_type == "from-or-to-accounting"):
            return Response(MemberVenderDetailModel.objects.filter(user= request.user).values("name"))
