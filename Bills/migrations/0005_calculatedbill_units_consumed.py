# Generated by Django 4.2.2 on 2023-09-02 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bills', '0004_rename_calculatedbills_calculatedbill'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculatedbill',
            name='units_consumed',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
