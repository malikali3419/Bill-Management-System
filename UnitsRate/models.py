from django.db import models

# Create your models here.
class CommercialUnitRates(models.Model):
    commercial_unit_price = models.DecimalField(default=0, max_digits=10,decimal_places=2, null=True, blank=True)

class ResidentialUnitRates(models.Model):
    residential_unit_price = models.DecimalField(default=0, max_digits=10,decimal_places=2, null=True, blank=True)

class FineAfterDueDate(models.Model):
    fine_after_due_date = models.DecimalField(default=0,max_digits=10,decimal_places=2, null=True, blank=True)

class MiscellaneousCharges(models.Model):
    miscellaneous_charges = models.DecimalField(default=0, max_digits=10,decimal_places=2, null=True, blank=True)


class UnitValues200OrLess(models.Model):
    range_for_200_or_less_residential = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    unit_price_for_200_less_units_residentails = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    range_for_200_or_less_commercial = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    unit_price_for_200_less_units_commercial = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)


class UnitValues400OrLess(models.Model):
    range_for_400_or_less_residentials = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    unit_price_for_400_less_units_residentials = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    range_for_400_or_less_commercial = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    unit_price_for_400_less_units_commercial = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)


class UnitValues600OrLess(models.Model):
    range_for_600_or_less_residentials = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    unit_price_for_600_less_units_residentials = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    range_for_600_or_less_commercial = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    unit_price_for_600_less_units_commercial = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

