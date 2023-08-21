from django.db import models
from Bills.models import *

# Create your models here.
class BillReadings(models.Model):
    bill = models.ForeignKey(Meter, on_delete=models.CASCADE)
    bill_reading = models.CharField(max_length=150, default=None, null=True)
    bill_amount = models.IntegerField(default=0, null=True)
