from django.http import request, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.db.models import Q
from django.db.models import Sum
import json
from datetime import datetime, timedelta

from accounting.models import ExpenseCategoryModel, IncomeCategoryModel, MemberVenderDetailModel, \
    SocietyMemberDetailsModel, \
    BalanceModel, IncomeExpenseLedgerModel, LedgerFile
from accounting.forms import MemberDetailsForm, CashWithdrawalForm, CashDepositForm
from accounting.resources import IncomeCategoryResource, ExpenseCategoryResource, SocietyMemberDetailsResource, \
    MemberVenderDetailResource, IncomeExpenseLedgerResource


# Create your views here.
class Dashboard(LoginRequiredMixin, View):

    def get(self, request):
        context = {}
        try:
            context['cash_balance'] = BalanceModel.objects.filter(user=request.user,
                                                                  account="Cash").first().balance_amount
            context['bank_balance'] = BalanceModel.objects.filter(user=request.user,
                                                                  account="Bank").first().balance_amount
            context['total_income'] = \
            IncomeExpenseLedgerModel.objects.filter(user=request.user, type="Income").aggregate(Sum("amount"))[
                'amount__sum']
            context['total_expense'] = \
            IncomeExpenseLedgerModel.objects.filter(user=request.user, type="Expense").aggregate(Sum("amount"))[
                'amount__sum']
            context['income'] = IncomeExpenseLedgerModel.objects.filter(user=request.user, type="Income")
            context['expense'] = IncomeExpenseLedgerModel.objects.filter(user=request.user, type="Expense")
            context["top_20_income"] = IncomeExpenseLedgerModel.objects.filter(user=request.user,
                                                                               type="Income").order_by('-amount')[:20]
            context["top_20_expense"] = IncomeExpenseLedgerModel.objects.filter(user=request.user,
                                                                                type="Expense").order_by('-amount')[:20]
            context["top_income_members"] = IncomeExpenseLedgerModel.objects.filter(user=request.user,
                                                                                    type="Income").values(
                "from_or_to_account").annotate(amount=Sum("amount"))
            context["top_expense_members"] = IncomeExpenseLedgerModel.objects.filter(user=request.user,
                                                                                     type="Expense").values(
                "from_or_to_account").annotate(amount=Sum("amount"))

        except Exception as e:
            pass
        return render(request, 'accounting/dashboard.html', context)


class IncomeCategory(LoginRequiredMixin, TemplateView):
    template_name = "accounting/income-category.html"


class IncomeCategoryCreateView(LoginRequiredMixin, CreateView):
    model = IncomeCategoryModel
    fields = ["category"]
    template_name = "accounting/income-category-add.html"

    def get_success_url(self):
        return reverse_lazy('income-category')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super(IncomeCategoryCreateView, self).form_valid(form)
        except IntegrityError:
            return self.form_invalid(form)


class IncomeCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = IncomeCategoryModel
    fields = ["category"]
    template_name = "accounting/income-category-update.html"

    def get_success_url(self):
        return reverse_lazy('income-category')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super(IncomeCategoryUpdateView, self).form_valid(form)
        except IntegrityError:
            return super().form_invalid(form)


class IncomeCategoryExportView(LoginRequiredMixin, View):

    def get(self, request):
        resource = IncomeCategoryResource()
        queryset = IncomeCategoryModel.objects.filter(user=request.user)
        dataset = resource.export(queryset)
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="income-category.xlsx"'
        return response


class ExpenseCategory(LoginRequiredMixin, TemplateView):
    template_name = "accounting/expense-category.html"


class ExpenseCategoryCreateView(LoginRequiredMixin, CreateView):
    model = ExpenseCategoryModel
    fields = ["category"]
    template_name = "accounting/expense-category-add.html"

    def get_success_url(self):
        return reverse_lazy('expense-category')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super(ExpenseCategoryCreateView, self).form_valid(form)
        except IntegrityError:
            return self.form_invalid(form)


class ExpenseCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = ExpenseCategoryModel
    fields = ["category"]
    template_name = "accounting/expense-category-update.html"

    def get_success_url(self):
        return reverse_lazy('expense-category')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super(ExpenseCategoryUpdateView, self).form_valid(form)
        except IntegrityError:
            return self.form_invalid(form)


class ExpenseCategoryExportView(LoginRequiredMixin, View):

    def get(self, request):
        resource = ExpenseCategoryResource()
        queryset = ExpenseCategoryModel.objects.filter(user=request.user)
        dataset = resource.export(queryset)
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="expense-category.xlsx"'
        return response


class MembersVender(LoginRequiredMixin, TemplateView):
    template_name = "accounting/members-vendor.html"


class MembersVenderCreateView(LoginRequiredMixin, CreateView):
    model = MemberVenderDetailModel
    fields = ["name"]
    template_name = "accounting/members-vendor-add.html"

    def get_success_url(self):
        return reverse_lazy('members-vendor')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super(MembersVenderCreateView, self).form_valid(form)
        except IntegrityError:
            return self.form_invalid(form)


class MembersVenderUpdateView(LoginRequiredMixin, UpdateView):
    model = MemberVenderDetailModel
    fields = ["name"]
    template_name = "accounting/members-vendor-update.html"

    def get_success_url(self):
        return reverse_lazy('members-vendor')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super(MembersVenderUpdateView, self).form_valid(form)
        except IntegrityError:
            return self.form_invalid(form)


class MembersVenderExportView(LoginRequiredMixin, View):

    def get(self, request):
        resource = MemberVenderDetailResource()
        queryset = MemberVenderDetailModel.objects.filter(user=request.user)
        dataset = resource.export(queryset)
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="member-vendor.xlsx"'
        return response


class MemberDetails(LoginRequiredMixin, TemplateView):
    template_name = "accounting/member-details.html"


class MemberDetailsCreateView(LoginRequiredMixin, CreateView):
    model = SocietyMemberDetailsModel
    form_class = MemberDetailsForm
    template_name = "accounting/member-details-add.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super(MemberDetailsCreateView, self).form_valid(form)
        except IntegrityError:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('member-details')


class MemberDetailsUpdateView(LoginRequiredMixin, UpdateView):
    model = SocietyMemberDetailsModel
    form_class = MemberDetailsForm
    template_name = "accounting/member-details-update.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super(MemberDetailsUpdateView, self).form_valid(form)
        except IntegrityError:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('member-details')


class MemberDetailsExportView(LoginRequiredMixin, View):

    def get(self, request):
        resource = SocietyMemberDetailsResource()
        queryset = SocietyMemberDetailsModel.objects.filter(user=request.user)
        dataset = resource.export(queryset)
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="society-members.xlsx"'
        return response


class Balance(LoginRequiredMixin, TemplateView):
    template_name = "accounting/balance.html"


class BalanceCreateView(LoginRequiredMixin, CreateView):
    model = BalanceModel
    fields = ["account", "balance_amount"]
    template_name = "accounting/balance-add.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super(BalanceCreateView, self).form_valid(form)
        except IntegrityError:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('balance')


class BalanceUpdateView(LoginRequiredMixin, UpdateView):
    model = BalanceModel
    fields = ["account", "balance_amount"]
    template_name = "accounting/balance-update.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super(BalanceUpdateView, self).form_valid(form)
        except IntegrityError:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('balance')


class IncomeExpenseLedger(LoginRequiredMixin, TemplateView):
    template_name = "accounting/ledger.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['income_category'] = IncomeCategoryModel.objects.filter(user=self.request.user)
        data['expense_category'] = ExpenseCategoryModel.objects.filter(user=self.request.user)
        data['member'] = MemberVenderDetailModel.objects.filter(user=self.request.user)
        return data


class IncomeExpenseLedgerCreateView(LoginRequiredMixin, CreateView):
    model = IncomeExpenseLedgerModel
    fields = ['date', 'transaction_type', 'type', 'category_header', 'amount', 'from_or_to_account',
              'transaction_details', 'voucherNo_or_invoiceNo', 'remark']
    template_name = "accounting/ledger-add.html"

    def add_balance_cash(self, request, transaction_type, amount, income_or_expense):
        if (income_or_expense == "Income"):
            if transaction_type == "Cash":
                opening_balance_cash = BalanceModel.objects.filter(user=request.user,
                                                                   account="Cash").first().balance_amount
                balance_model_instance = BalanceModel.objects.filter(user=request.user, account="Cash").first()
                balance_model_instance.balance_amount += amount
                balance_model_instance.save()
                closing_balance_cash = balance_model_instance.balance_amount
                opening_balance_bank = BalanceModel.objects.filter(user=request.user,
                                                                   account="Bank").first().balance_amount
                closing_balance_bank = BalanceModel.objects.filter(user=request.user,
                                                                   account="Bank").first().balance_amount
                return opening_balance_cash, closing_balance_cash, opening_balance_bank, closing_balance_bank

            elif transaction_type == "Bank":
                opening_balance_bank = BalanceModel.objects.filter(user=request.user,
                                                                   account="Bank").first().balance_amount
                balance_model_instance = BalanceModel.objects.filter(user=request.user, account="Bank").first()
                balance_model_instance.balance_amount += amount
                balance_model_instance.save()
                closing_balance_bank = balance_model_instance.balance_amount
                opening_balance_cash = BalanceModel.objects.filter(user=request.user,
                                                                   account="Cash").first().balance_amount
                closing_balance_cash = BalanceModel.objects.filter(user=request.user,
                                                                   account="Cash").first().balance_amount
                return opening_balance_cash, closing_balance_cash, opening_balance_bank, closing_balance_bank

        elif (income_or_expense == "Expense"):
            if transaction_type == "Cash":
                opening_balance_cash = BalanceModel.objects.filter(user=request.user,
                                                                   account="Cash").first().balance_amount
                balance_model_instance = BalanceModel.objects.filter(user=request.user, account="Cash").first()
                balance_model_instance.balance_amount -= amount
                balance_model_instance.save()
                closing_balance_cash = balance_model_instance.balance_amount
                opening_balance_bank = BalanceModel.objects.filter(user=request.user,
                                                                   account="Bank").first().balance_amount
                closing_balance_bank = BalanceModel.objects.filter(user=request.user,
                                                                   account="Bank").first().balance_amount
                return opening_balance_cash, closing_balance_cash, opening_balance_bank, closing_balance_bank

            elif transaction_type == "Bank":
                opening_balance_bank = BalanceModel.objects.filter(user=request.user,
                                                                   account="Bank").first().balance_amount
                balance_model_instance = BalanceModel.objects.filter(user=request.user, account="Bank").first()
                balance_model_instance.balance_amount -= amount
                balance_model_instance.save()
                closing_balance_bank = balance_model_instance.balance_amount
                opening_balance_cash = BalanceModel.objects.filter(user=request.user,
                                                                   account="Cash").first().balance_amount
                closing_balance_cash = BalanceModel.objects.filter(user=request.user,
                                                                   account="Cash").first().balance_amount
                return opening_balance_cash, closing_balance_cash, opening_balance_bank, closing_balance_bank

        elif (income_or_expense == "CASH OUT"):
            bank = BalanceModel.objects.filter(user=request.user, account="Bank").first()
            cash = BalanceModel.objects.filter(user=request.user, account="Cash").first()

            opening_balance_cash = cash.balance_amount
            opening_balance_bank = bank.balance_amount

            bank.balance_amount = bank.balance_amount - amount
            bank.save()
            cash.balance_amount = cash.balance_amount + amount
            cash.save()

            closing_balance_cash = cash.balance_amount
            closing_balance_bank = bank.balance_amount
            return opening_balance_cash, closing_balance_cash, opening_balance_bank, closing_balance_bank

        elif (income_or_expense == "CASH IN"):
            bank = BalanceModel.objects.filter(user=request.user, account="Bank").first()
            cash = BalanceModel.objects.filter(user=request.user, account="Cash").first()

            opening_balance_cash = cash.balance_amount
            opening_balance_bank = bank.balance_amount

            bank.balance_amount = bank.balance_amount + amount
            bank.save()
            cash.balance_amount = cash.balance_amount - amount
            cash.save()

            closing_balance_cash = cash.balance_amount
            closing_balance_bank = bank.balance_amount
            return opening_balance_cash, closing_balance_cash, opening_balance_bank, closing_balance_bank

    def form_valid(self, form):
        form.instance.user = self.request.user
        transaction_type = form.instance.transaction_type
        amount = form.instance.amount
        income_or_expense = form.instance.type
        try:
            opening_balance_cash, closing_balance_cash, opening_balance_bank, closing_balance_bank = self.add_balance_cash(
                self.request, transaction_type, amount, income_or_expense)
        except:
            return self.form_invalid(form)
        form.instance.opening_balance_cash = opening_balance_cash
        form.instance.closing_balance_cash = closing_balance_cash
        form.instance.opening_balance_bank = opening_balance_bank
        form.instance.closing_balance_bank = closing_balance_bank
        try:
            return super(IncomeExpenseLedgerCreateView, self).form_valid(form)
        except IntegrityError:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('income-expense-ledger')


class IncomeExpenseLedgerUpdateView(LoginRequiredMixin, UpdateView):
    model = IncomeExpenseLedgerModel
    fields = ['date', 'type', 'amount', 'category_header', 'from_or_to_account', 'transaction_type',
              'transaction_details', 'voucherNo_or_invoiceNo', 'remark']
    template_name = "accounting/ledger-update.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super(IncomeExpenseLedgerUpdateView, self).form_valid(form)
        except IntegrityError:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('income-expense-ledger')


class IncomeExpenseLedgerExportView(LoginRequiredMixin, View):

    def get(self, request):
        resource = IncomeExpenseLedgerResource()
        queryset = IncomeExpenseLedgerModel.objects.filter(user=request.user)
        dataset = resource.export(queryset)
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="income-expense-ledger.xlsx"'
        return response


class FilteredIncomeExpenseLedgerExportView(LoginRequiredMixin, View):

    def get(self, request):
        resource = IncomeExpenseLedgerResource()
        qs = IncomeExpenseLedgerModel.objects.filter(user=request.user)
        if self.request.GET:
            data = dict(self.request.GET)
            for i in data:
                if i == "transaction_type":
                    qs = qs.filter(Q(transaction_type__contains=data[i][0]))
                if i == "category_header":
                    qs = qs.filter(Q(category_header__contains=data[i][0]))
                if i == "member":
                    qs = qs.filter(Q(from_or_to_account__contains=data[i][0]))
                if i == "type":
                    qs = qs.filter(Q(type__contains=data[i][0]))
                if i == "start":
                    if data[i][0]:
                        qs = qs.filter(Q(created__date__gte=datetime.strptime(data[i][0], "%Y-%m-%d")))
                if i == "end":
                    if data[i][0]:
                        qs = qs.filter(Q(created__date__lte=datetime.strptime(data[i][0], "%Y-%m-%d")))

        dataset = resource.export(qs)
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="income-expense-ledger.xlsx"'
        return response


class UploadExcel(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'accounting/upload-excel.html')


class CashWithdrawalView(LoginRequiredMixin, View):

    def get(self, request):
        context = {}
        context['form'] = CashWithdrawalForm
        return render(request, "accounting/cash-withdrawal.html", context)

    def post(self, request):
        amount = int(request.POST.get("amount"))
        bank = BalanceModel.objects.filter(user=request.user, account="bank").first()
        cash = BalanceModel.objects.filter(user=request.user, account="cash").first()

        if (amount < bank.balance_amount):
            opening_balance_cash = cash.balance_amount
            opening_balance_bank = bank.balance_amount

            bank.balance_amount = bank.balance_amount - amount
            bank.save()
            cash.balance_amount = cash.balance_amount + amount
            cash.save()

            closing_balance_cash = cash.balance_amount
            closing_balance_bank = bank.balance_amount
            IncomeExpenseLedgerModel.objects.create(
                user=request.user,
                date=request.POST.get('date'),
                amount=amount,
                transaction_details=request.POST.get('transaction_details'),
                opening_balance_cash=opening_balance_cash,
                closing_balance_cash=closing_balance_cash,
                opening_balance_bank=opening_balance_bank,
                closing_balance_bank=closing_balance_bank
            )
            return redirect('income-expense-ledger')
        else:
            return redirect('income-expense-ledger')


class CashDepositView(LoginRequiredMixin, View):

    def get(self, request):
        context = {}
        context['form'] = CashDepositForm
        return render(request, "accounting/cash-deposit.html", context)

    def post(self, request):
        amount = int(request.POST.get("amount"))
        bank = BalanceModel.objects.filter(user=request.user, account="bank").first()
        cash = BalanceModel.objects.filter(user=request.user, account="cash").first()

        if (amount < cash.balance_amount):
            opening_balance_cash = cash.balance_amount
            opening_balance_bank = bank.balance_amount

            bank.balance_amount = bank.balance_amount + amount
            bank.save()
            cash.balance_amount = cash.balance_amount - amount
            cash.save()

            closing_balance_cash = cash.balance_amount
            closing_balance_bank = bank.balance_amount
            IncomeExpenseLedgerModel.objects.create(
                user=request.user,
                date=request.POST.get('date'),
                amount=amount,
                transaction_details=request.POST.get('transaction_details'),
                opening_balance_cash=opening_balance_cash,
                closing_balance_cash=closing_balance_cash,
                opening_balance_bank=opening_balance_bank,
                closing_balance_bank=closing_balance_bank
            )
            return redirect('income-expense-ledger')
        else:
            return redirect('income-expense-ledger')


class UploadLedgerFileView(LoginRequiredMixin, CreateView):
    model = LedgerFile
    fields = ("file",)
    template_name = "accounting/upload-ledger-file.html"

    def form_valid(self, form):
        pk = self.request.get_raw_uri().split("/")[-1]
        ledger_record = IncomeExpenseLedgerModel.objects.get(pk=pk)
        form.instance.ledger_record = ledger_record
        try:
            return super(UploadLedgerFileView, self).form_valid(form)
        except IntegrityError:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('income-expense-ledger')
