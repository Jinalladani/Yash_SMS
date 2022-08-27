from django import forms
from phonenumber_field.formfields import PhoneNumberField

class MemberLoginForm(forms.Form):
    mobile_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Enter Mobile Number'}), required= True)