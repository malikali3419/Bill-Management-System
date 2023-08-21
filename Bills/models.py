from django.db import models
from Area.models import Areas

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

    house = models.ForeignKey(Areas, null=True, blank=True, on_delete=models.CASCADE)
    meter_id = models.CharField(max_length=50, default=None, null=True, blank=True)
    meter_owner = models.CharField(max_length=50, default=None, null=True, blank=True)
    meter_type = models.CharField(choices=METER_TYPE_CHOICES,default='E', max_length=30)
   

    def __str__(self) -> str:
        return str(self.meter_id)
    
class CalculatedBills(TimestampedModel):
    BILL_STATUS_CHOICES = [
        ('paid','Paid'),
        ('unpaid','Unpaid')
    ]
    meter = models.ForeignKey(Meter, null=True, blank=True, on_delete=models.CASCADE)
    bill_id = models.CharField(max_length=50, default=None, null=True, blank=True)
    bill_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    bill_reading_img = models.ImageField(upload_to='./images', default=None)
    bill_reading = models.CharField(max_length=100, default=0, null=True, blank=True)
    bill_status = models.CharField(choices=BILL_STATUS_CHOICES, max_length=50, default=None, null=True, blank=True)
    payment_recieved = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    remaing_dues = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.bill_id)
    

