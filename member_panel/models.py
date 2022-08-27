from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class OtpModel(models.Model):
    mobile_number = PhoneNumberField()
    otp = models.CharField(max_length=6)