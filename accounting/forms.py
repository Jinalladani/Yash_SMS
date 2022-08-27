from django import forms
from django.forms import ModelForm, Form
from accounting.models import SocietyMemberDetailsModel, LedgerFile

class MemberDetailsForm(ModelForm):

    class Meta:
        model = SocietyMemberDetailsModel
        exclude = ('user',)

class CashWithdrawalForm(Form):
    date = forms.DateField(label='Date', required=True)
    amount = forms.IntegerField(label="Enter Amount", required=True)
    transaction_details = forms.CharField(label="Transaction Details", required=False)

class CashDepositForm(Form):
    date = forms.DateField(label='Date', required=True)
    amount = forms.IntegerField(label="Enter Amount", required=True)
    transaction_details = forms.CharField(label="Transaction Details", required=False)