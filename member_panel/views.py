from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q
from django.conf import settings
import requests
from random import randint
import phonenumbers
from django.contrib import messages
from django.db.models import Sum

from accounting.models import SocietyMemberDetailsModel
from authentication.models import User
from member_panel.forms import MemberLoginForm
from member_panel.models import OtpModel
from accounting.models import SocietyMemberDetailsModel, \
    BalanceModel, IncomeExpenseLedgerModel, IncomeCategoryModel, ExpenseCategoryModel, MemberVenderDetailModel

from member_panel.mixins import MemberLoginRequired, RedirectIfLoggedIn

class SocietyListView(MemberLoginRequired, TemplateView):

    def get(self, request):
        context = {}
        mobile_number = request.session["mobile_number"]
        mobile_number = phonenumbers.parse(mobile_number, None)
        Member = SocietyMemberDetailsModel.objects.filter(Q(primary_contact_no= mobile_number) | Q(secondary_contact_no= mobile_number) | Q(whatsapp_contact_no= mobile_number))
        context['members'] = Member
        return render(request, "member-panel/member-society-list.html", context)

class MemberDashboard(MemberLoginRequired, TemplateView):

    def get(self, request, pk):
        context = {}
        society = User.objects.get(pk= pk)
        request.session["society-id"] = society.pk
        context['society'] = society
        context['cash_balance'] = BalanceModel.objects.filter(user= society, account="Cash").first().balance_amount
        context['bank_balance'] = BalanceModel.objects.filter(user= society, account="Bank").first().balance_amount
        context['total_income'] = IncomeExpenseLedgerModel.objects.filter(user= society, type="Income").aggregate(Sum("amount"))['amount__sum']
        context['total_expense'] = IncomeExpenseLedgerModel.objects.filter(user= society, type="Expense").aggregate(Sum("amount"))['amount__sum']
        return render(request, "member-panel/member-dashboard.html", context)

class MemberDashboardDetailView(MemberLoginRequired, TemplateView):

    def get(self, request, detail_type):
        context = {}
        pk = request.session["society-id"]
        society = User.objects.get(pk= pk)
        context['society'] = society
        if detail_type == "income_details":
            context['income'] = IncomeExpenseLedgerModel.objects.filter(user= society, type="Income")
            return render(request, "member-panel/income-details.html", context)

        if detail_type == "expense_details":
            context['expense'] = IncomeExpenseLedgerModel.objects.filter(user= society, type="Expense")
            return render(request, "member-panel/expense-details.html", context)

        if detail_type == "top_20_expense_details":
            context["top_20_expense"] = IncomeExpenseLedgerModel.objects.filter(user= society, type="Expense").order_by('-amount')[:20]
            return render(request, "member-panel/top-20-expense-details.html", context)

        if detail_type == "top_20_income_details":
            context["top_20_income"] = IncomeExpenseLedgerModel.objects.filter(user= society, type="Income").order_by('-amount')[:20]
            return render(request, "member-panel/top-20-income-details.html", context)

        if detail_type == "top_income_member_details":
            context["top_income_members"] = IncomeExpenseLedgerModel.objects.filter(user= society, type="Income").values("from_or_to_account").annotate(amount= Sum("amount"))
            return render(request, "member-panel/top-income-member-details.html", context)

        if detail_type == "top_expense_member_details":
            context["top_expense_members"] = IncomeExpenseLedgerModel.objects.filter(user= society, type="Expense").values("from_or_to_account").annotate(amount= Sum("amount"))
            return render(request, "member-panel/top-expense-member-details.html", context)

class MemberIncomeExpenseLedger(MemberLoginRequired, TemplateView):

    def get(self, request, pk):
        context = {}
        society = User.objects.get(pk= pk)
        context['society'] = society
        context['income_category'] = IncomeCategoryModel.objects.filter(user= society)
        context['expense_category'] = ExpenseCategoryModel.objects.filter(user= society)
        context['member'] = MemberVenderDetailModel.objects.filter(user= society)
        return render(request, "member-panel/member-income-expense-ledger.html", context)

class MemberLoginView(RedirectIfLoggedIn, View):

    def get(self, request):
        context = {}
        form = MemberLoginForm()
        context['form'] = form
        return render(request, "member-panel/member-login.html", context)

    def post(self, request):
        context = {}
        form = MemberLoginForm(request.POST)

        if form.is_valid():
            mobile_number = form.cleaned_data["mobile_number"]
            Member = SocietyMemberDetailsModel.objects.filter(Q(primary_contact_no= mobile_number) | Q(secondary_contact_no= mobile_number) | Q(whatsapp_contact_no= mobile_number))
            try:
                if Member:
                    otp = randint(100000, 999999)
                    requests.get(settings.SMSURL.format(phone_no= mobile_number, otp= otp))
                    obj, created = OtpModel.objects.update_or_create(mobile_number= mobile_number, defaults={"otp": otp})
                    request.session['mobile_number'] = mobile_number.raw_input
                    return redirect("member-otp-verification")
                else:
                    form.add_error(None, "Mobile Number is not registered.")
                    context['form'] = form
                    return render(request, "member-panel/member-login.html", context)
            except Exception as e:
                print(e)
        else:
            context['form'] = form
            return render(request, "member-panel/member-login.html", context)

class MemberOtpVerification(RedirectIfLoggedIn, View):

    def get(self, request):
        context = {}
        return render(request, "member-panel/member-otp-verification.html", context)

    def post(self, request):
        context = {}
        otp = request.POST.get("otp")
        mobile_number = phonenumbers.parse(request.session['mobile_number'], None)

        stored_otp = OtpModel.objects.filter(mobile_number= mobile_number).first().otp

        if int(stored_otp) == int(otp):
            request.session["is_verified"] = True
            return redirect('member-society-list')
        else:
            request.session["is_verified"] = False
            messages.add_message(request, messages.INFO, "OTP is not valid.")
            return render(request, "member-panel/member-otp-verification.html", context)

class MemberLogoutView(MemberLoginRequired, View):

    def get(self, request):
        del request.session["mobile_number"]
        del request.session["is_verified"]
        return redirect("member-login")