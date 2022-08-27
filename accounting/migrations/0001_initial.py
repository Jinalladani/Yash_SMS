# Generated by Django 3.2.6 on 2021-12-21 16:11

import accounting.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomeExpenseLedgerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('date', models.DateField()),
                ('type', models.CharField(choices=[('', '----------'), ('Income', 'Income'), ('Expense', 'Expense'), ('CASH OUT', 'CASH OUT'), ('CASH IN', 'CASH IN')], max_length=100)),
                ('amount', models.FloatField(max_length=100)),
                ('category_header', models.CharField(blank=True, max_length=100, null=True)),
                ('from_or_to_account', models.CharField(blank=True, max_length=100, null=True)),
                ('transaction_type', models.CharField(choices=[('Cash', 'Cash'), ('Bank', 'Bank')], max_length=100)),
                ('transaction_details', models.CharField(blank=True, max_length=100, null=True)),
                ('voucherNo_or_invoiceNo', models.CharField(blank=True, max_length=100, null=True)),
                ('remark', models.TextField(blank=True, max_length=500, null=True)),
                ('opening_balance_cash', models.FloatField(max_length=100)),
                ('closing_balance_cash', models.FloatField(max_length=100)),
                ('opening_balance_bank', models.FloatField(max_length=100)),
                ('closing_balance_bank', models.FloatField(max_length=100)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='IncomeExpenseLedger', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MemberVenderDetailModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='MemberVenderDetail', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LedgerFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('file', models.FileField(upload_to=accounting.models.user_directory_path, verbose_name='Income expense ledger file')),
                ('ledger_record', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='LedgerFile', to='accounting.incomeexpenseledgermodel')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SocietyMemberDetailsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('flat_no', models.CharField(max_length=200)),
                ('primary_name', models.CharField(blank=True, max_length=200, null=True)),
                ('primary_contact_no', models.CharField(blank=True, max_length=10, null=True)),
                ('secondary_name', models.CharField(blank=True, max_length=200, null=True)),
                ('secondary_contact_no', models.CharField(blank=True, max_length=10, null=True)),
                ('accounting_name', models.CharField(blank=True, max_length=200, null=True)),
                ('whatsapp_contact_no', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('residence', models.CharField(choices=[('owner', 'Owner'), ('rental', 'Rental'), ('wenter', 'Wenter')], max_length=100)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='SocietyMemberDetails', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'flat_no')},
            },
        ),
        migrations.CreateModel(
            name='IncomeCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('category', models.CharField(max_length=200)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='IncomeCategory', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'category')},
            },
        ),
        migrations.CreateModel(
            name='ExpenseCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('category', models.CharField(max_length=200)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ExpenseCategory', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'category')},
            },
        ),
        migrations.CreateModel(
            name='BalanceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('account', models.CharField(choices=[('Cash', 'Cash'), ('Bank', 'Bank')], max_length=20)),
                ('balance_amount', models.FloatField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Balance', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'account')},
            },
        ),
    ]