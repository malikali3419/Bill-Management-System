# Generated by Django 3.2.20 on 2023-08-27 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UnitsRate', '0003_auto_20230812_2023'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitValues200OrLess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('range_for_200_or_less_residential', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('unit_price_for_200_less_units_residentails', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('range_for_200_or_less_commercial', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('unit_price_for_200_less_units_commercial', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnitValues400OrLess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('range_for_400_or_less_residentials', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('unit_price_for_400_less_units_residentials', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('range_for_400_or_less_commercial', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('unit_price_for_400_less_units_commercial', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnitValues600OrLess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('range_for_600_or_less_residentials', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('unit_price_for_600_less_units_residentials', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('range_for_600_or_less_commercial', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('unit_price_for_600_less_units_commercial', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
            ],
        ),
    ]
