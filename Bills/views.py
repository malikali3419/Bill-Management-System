from django.shortcuts import render
from .models import Meter, CalculatedBills
from Area.models import Areas
from UnitsRate.models import *
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime, timedelta

# Create your views here.
from django.views.generic.detail import View
class ShowMeters(View):
    def get(self,request,*args, **kwargs):
        context = {}
        area_id = kwargs.get('area_id', None) 
        meters = Meter.objects.filter(
            house__id=area_id
        )
        context['meters'] = meters
        
        if request.user.role == 'Meter Reader':
            return render(request, 'MeterReader/show-meters.html', context)
        if request.user.role == 'Manager':
            return render(request, 'Manager/show-meters.html', context)
    
class ShowMetersDetails(View):
    def get(self,request,*args, **kwargs):
        meter_id = kwargs.get('meter_id', None)
        meter = Meter.objects.filter(
            id=meter_id
        ).first()
        house = meter.house.house_number
        context = {}
        total_amount = 0
        bills = CalculatedBills.objects.filter(
            meter__id=meter.id,
            bill_status='Unpaid'
        )
        print(bills[0].created_at)
        for bill in bills:
            provided_date = str(bill.created_at)
            print(provided_date)
           
            current_date = datetime.now().date()
           
            provided_datetime = datetime.strptime(provided_date, "%Y-%m-%d %H:%M:%S.%f%z")
            date_after_10_days = provided_datetime + timedelta(days=10)

            # Sample current_date for demonstration purposes
            current_date_str = str(current_date)
            current_date = datetime.strptime(current_date_str, '%Y-%m-%d')

            # Convert the offset-naive datetime to be offset-aware using the timezone of provided_datetime
            current_date_aware = current_date.replace(tzinfo=provided_datetime.tzinfo)
             
            print(current_date_aware)
            print(date_after_10_days)
            if current_date_aware > date_after_10_days:
                context['message'] = 'Inclding Fine After Due date'
                total_amount += float(bill.bill_total_amount) * (float(FineAfterDueDate.objects.all().first().fine_after_due_date/100))
            total_amount_bills = bills.aggregate(bill_total_amount=Sum('bill_total_amount'))['bill_total_amount']
            
            total_amount += float(total_amount_bills)
        context['meter'] = meter
        context['house'] = house
        if request.user.role == 'Meter Reader':
            return render(request, 'MeterReader/meter_details.html', context)
        if request.user.role == 'Manager':
            context['bills'] = bills
            context['total_amount'] = total_amount
            return render(request, 'Manager/meter_details.html', context)
    
    def post(self,request,*args, **kwargs):
        if request.user.role == "Meter Reader":
            meter_id = kwargs.get('meter_id', None)
            bill_image = request.FILES.get('meter_img', None)
            bill_reading = request.POST.get('meter_reading', None)
            meter = Meter.objects.filter(
                id=meter_id
            ).first()
            bill = CalculatedBills.objects.filter(
                meter__id=meter_id
            ).last()
            print(bill.bill_reading)
            bill_total_reading = int(bill_reading) -  int(bill.bill_reading) 
            print(bill_total_reading)
            bill_total_amount = 0
            if meter.house.area_type == 'commercial':
                if bill.bill_status == "Unpaid":
                    bill_total_amount = float(bill.bill_total_amount)
                bill_total_amount += bill_total_reading * float(CommercialUnitRates.objects.all().first().commercial_unit_price)
            else:
                if bill.bill_status == "Unpaid":
                    bill_total_amount = float(bill.bill_total_amount)
                bill_total_amount += bill_total_reading * float(ResidentialUnitRates.objects.all().first().residential_unit_price)
            bill_total_amount += float(MiscellaneousCharges.objects.all().first().miscellaneous_charges)
            try:
                bill = CalculatedBills(
                    meter=meter,
                    bill_id=meter.meter_id,
                    bill_total_amount=bill_total_amount,
                    bill_reading_img=bill_image,
                    bill_reading=bill_reading,
                    bill_status='Unpaid'
                )
                bill.save()
                messages.success(request, "Succes")
            except Exception as e:
                print(e)
                messages.error(request, 'Error')
            print(meter_id)
            return render(request, 'MeterReader/meter_details.html')
        elif request.user.role == 'Manager':
            meter_id = kwargs.get('meter_id', None)
            total_amount = float(request.POST.get('total_amount', None))
            recieved_amount = float(request.POST.get('r_amount', None))
            print(total_amount, recieved_amount)
            bills = CalculatedBills.objects.filter(
                meter__id=meter_id
            )
            if int(total_amount) == int(recieved_amount):
                try:
                    for bill in bills:
                        bill.bill_status = 'Paid'
                        bill.remaing_dues = 0
                        bill.save()
                    messages.success(request, "Succes")
                except Exception as e:
                    print(e)
                    messages.error(request, "Error")

            else:
                pass
            return render(request, 'Manager/meter_details.html')
        return render(request, '404-error.html')
        



        







