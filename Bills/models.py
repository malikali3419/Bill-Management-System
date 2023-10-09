from django.db import models
from Area.models import Area
from datetime import datetime, timedelta, timezone

# Create your models here.


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  

class Meter(TimestampedModel):
    METER_TYPE_CHOICES = [
        ('Electicity', 'Electricity'),
        ('Gas', 'Gas'),
        ('Water', 'Water'),
    ]

    house = models.ForeignKey(Area, null=True, blank=True, on_delete=models.CASCADE)
    meter_id = models.CharField(max_length=50, default=None, null=True, blank=True)
    meter_owner = models.CharField(max_length=50, default=None, null=True, blank=True)
    meter_type = models.CharField(choices=METER_TYPE_CHOICES,default='E', max_length=30)
   

    def __str__(self) -> str:
        return str(self.meter_id)
    
class CalculatedBill(TimestampedModel):
    BILL_STATUS_CHOICES = [
        ('paid','Paid'),
        ('unpaid','Unpaid'),
        ('ipaid','Initialy Paid')
    ]
    meter = models.ForeignKey(Meter, null=True, blank=True, on_delete=models.CASCADE)
    bill_id = models.CharField(max_length=50, default=None, null=True, blank=True)
    bill_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    bill_reading_img = models.ImageField(upload_to='./images', default=None)
    bill_reading = models.CharField(max_length=100, default=0, null=True, blank=True)
    bill_status = models.CharField(choices=BILL_STATUS_CHOICES, max_length=50, default=None, null=True, blank=True)
    payment_recieved = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    units_consumed = models.CharField(max_length=100, default=None, null=True, blank=True)
    remaing_dues = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    def total_unit_of_this_month(self):
        today = datetime.now(timezone.utc)
        twenty_days_ago = today - timedelta(days=20)
        total_units = 0
        print(self.id)
        if self.created_at > twenty_days_ago:
            if self.units_consumed:
                total_units += int(self.units_consumed)
        return total_units

    def total_bill_of_this_month(self):
        today = datetime.now(timezone.utc)
        twenty_days_ago = today - timedelta(days=20)
        total_bill_amount = 0
        print(self.id)
        if self.created_at > twenty_days_ago:
            if self.bill_total_amount:
                total_bill_amount += int(self.bill_total_amount)
        return total_bill_amount
    
    def total_bill_recieved(self):
        today = datetime.now(timezone.utc)
        twenty_days_ago = today - timedelta(days=20)
        total_bill_amount = 0
        print(self.id)
        if self.created_at > twenty_days_ago:
            if self.bill_total_amount and (self.bill_status == 'paid' or self.bill_status == 'ipaid'):
                total_bill_amount += int(self.bill_total_amount)
        return total_bill_amount
    
    def total_bill_pending(self):
        today = datetime.now(timezone.utc)
        twenty_days_ago = today - timedelta(days=20)
        total_bill_amount = 0
        print(self.id)
        if self.created_at > twenty_days_ago:
            if self.bill_total_amount and (self.bill_status == 'unpaid' or self.bill_status == 'ipaid'):
                total_bill_amount += int(self.bill_total_amount) + int(self.remaing_dues)
        return total_bill_amount
    def __str__(self) -> str:
        return str(self.bill_id)
    

