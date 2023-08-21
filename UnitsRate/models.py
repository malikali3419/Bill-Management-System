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




