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

class DueDateForFine(models.Model):
    fine_date = models.DateField(default=None,blank=True, null=True)


class FirstRangeOfUnitValue(models.Model):
    range_of_units_residential = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    unit_price_for_first_range_residentails = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    range_of_units_commercial = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    unit_price_for_first_range_wdcommercial = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)


class SecondRangeOfUnitValue(models.Model):
    range_of_units_residential = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    unit_price_for_second_range_residentails = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    range_of_units_commercial = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    unit_price_for_second_range_wdcommercial = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)


class ThirdRangeOfUnitValue(models.Model):
    range_of_units_residential = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    unit_price_for_third_range_residentails = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    range_of_units_commercial = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    unit_price_for_third_range_wdcommercial = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

class FouthRangeOfUnitValue(models.Model):
    range_of_units_residential = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    unit_price_for_fourht_range_residentails = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    range_of_units_commercial = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    unit_price_for_fourth_range_wdcommercial = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

