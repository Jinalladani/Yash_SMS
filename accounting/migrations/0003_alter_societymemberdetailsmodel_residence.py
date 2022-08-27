# Generated by Django 3.2.6 on 2021-12-21 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_alter_societymemberdetailsmodel_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='societymemberdetailsmodel',
            name='residence',
            field=models.CharField(choices=[('owner', 'Owner'), ('rental', 'Rental'), ('wenter', 'Wenter')], max_length=100, null=True),
        ),
    ]
