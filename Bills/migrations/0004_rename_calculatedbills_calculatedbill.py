# Generated by Django 3.2.20 on 2023-08-26 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bills', '0003_alter_calculatedbills_bill_total_amount'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CalculatedBills',
            new_name='CalculatedBill',
        ),
    ]
