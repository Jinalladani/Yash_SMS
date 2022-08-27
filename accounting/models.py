from django.db import models
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

class ExpenseCategoryModel(TimeStampedModel):
    user = models.ForeignKey('authentication.User', related_name='ExpenseCategory', on_delete=models.CASCADE, blank=True, null=True)
    category = models.CharField(max_length=200)

    class Meta:
        unique_together = ('user', 'category',)

    def __str__(self) -> str:
        return self.category

class IncomeCategoryModel(TimeStampedModel):
    user = models.ForeignKey('authentication.User', related_name='IncomeCategory', on_delete=models.CASCADE, blank=True, null=True)
    category = models.CharField(max_length=200)

    class Meta:
        unique_together = ('user', 'category',)

    def __str__(self) -> str:
        return self.category

class BalanceModel(TimeStampedModel):
    ACCOUNT_TYPE = (
        ("Cash", "Cash"),
        ("Bank", "Bank"),
    )
    user = models.ForeignKey('authentication.User', related_name='Balance', on_delete=models.CASCADE, blank=True, null=True)
    account = models.CharField(max_length = 20,choices = ACCOUNT_TYPE)
    balance_amount = models.FloatField()

    class Meta:
        unique_together = ('user', 'account')

    def __str__(self) -> str:
        return self.account

class MemberVenderDetailModel(TimeStampedModel):
    user = models.ForeignKey('authentication.User', related_name='MemberVenderDetail', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class SocietyMemberDetailsModel(TimeStampedModel):
    RESIDENCE = (
        ("owner", "Owner"),
        ("rental", "Rental"),
        ("wenter", "Wenter")
    )

    user = models.ForeignKey('authentication.User', related_name='SocietyMemberDetails', on_delete=models.CASCADE, blank=True, null=True)
    flat_no = models.CharField(max_length=200)
    primary_name = models.CharField(max_length=200, null=True, blank=True)
    primary_contact_no = PhoneNumberField(null=True, blank=True)
    secondary_name = models.CharField(max_length=200, null=True, blank=True)
    secondary_contact_no = PhoneNumberField(null=True, blank=True)
    accounting_name = models.CharField(max_length=200, null=True, blank=True)
    whatsapp_contact_no = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(null=True)
    residence = models.CharField(max_length=100, choices=RESIDENCE, null=True)

    class Meta:
        unique_together = (
            ('user', 'flat_no')
        )

    def __str__(self) -> str:
        return self.primary_name

def user_directory_path(instance, filename):
    return f'leger_file_{instance.ledger_record.user.society_name}/{filename}' 

class IncomeExpenseLedgerModel(TimeStampedModel):
    ACCOUNT_TYPE = (
        ("Cash", "Cash"),
        ("Bank", "Bank"),
    )

    TYPE = (
        ("","----------"),
        ("Income", "Income"),
        ("Expense", "Expense"),
        ("CASH OUT", "CASH OUT"),
        ("CASH IN", "CASH IN")
    )
    
    user = models.ForeignKey('authentication.User', related_name='IncomeExpenseLedger', on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField()
    type = models.CharField(max_length=100, choices=TYPE)
    amount = models.FloatField(max_length=100)
    category_header = models.CharField(max_length=100, null=True, blank=True)
    from_or_to_account = models.CharField(max_length=100, null=True, blank=True)
    transaction_type = models.CharField(max_length=100, choices = ACCOUNT_TYPE)
    transaction_details = models.CharField(max_length=100, null=True, blank=True)
    voucherNo_or_invoiceNo = models.CharField(max_length=100, null=True, blank=True)
    remark = models.TextField(max_length=500, null=True, blank=True)
    opening_balance_cash = models.FloatField(max_length=100)
    closing_balance_cash = models.FloatField(max_length=100)
    opening_balance_bank = models.FloatField(max_length=100)
    closing_balance_bank = models.FloatField(max_length=100)

class LedgerFile(TimeStampedModel):
    ledger_record = models.ForeignKey('accounting.IncomeExpenseLedgerModel', related_name='LedgerFile', on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(upload_to=user_directory_path, verbose_name='Income expense ledger file')