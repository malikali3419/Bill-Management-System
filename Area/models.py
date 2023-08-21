
from django.db import models

# Create your models here.
from django.db import models

from datetime import datetime, timedelta, timezone

class Areas(models.Model):
    AREA_TYPE_CHOICES = [
        ('commercial','Commercial'),
        ('residential','Residential')
    ]
    BILL_STATUS_CHOICES =  [
        ('paid','Paid'),
        ('unpaid','Unpaid')
    ]

    id = models.AutoField(primary_key=True)  # Explicitly define the primary key

    owners_name = models.CharField(max_length=155, default=None, null=True, blank=True)
    house_number = models.CharField(max_length=15, default=None, null=True, blank=True)
    CNIC = models.CharField(max_length=20, default=None, null=True)
    area_block = models.CharField(max_length=10, default=None, null=True)
    meter_no = models.CharField(max_length=50, default=None, null=True)
    area_type = models.CharField(max_length=50, choices=AREA_TYPE_CHOICES, default='commercial')
    owners_phone_number = models.CharField(max_length=20, default=None, blank=True, null=True)
    bill_paid_status = models.CharField(max_length=155, choices=BILL_STATUS_CHOICES, default='unpaid')

    def __str__(self) -> str:
        return str(self.area_no)

    def is_reading_noted(self):
        from Bills.models import Meter, CalculatedBills
        today = datetime.now(timezone.utc)
        twenty_days_ago = today - timedelta(days=20)
        print(self.id)
        bill = CalculatedBills.objects.filter(meter__house__id=self.id).order_by('-created_at').first()
        if bill:
            print(bill)
            if bill.updated_at < twenty_days_ago:
                return False
            else:
                return True

    
class Block(models.Model):
    block_name = models.CharField(max_length=30, default=None, null=True, blank=True)
    def __str__(self) -> str:
        return self.block_name

