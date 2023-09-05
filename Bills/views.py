from django.shortcuts import render
from .models import Meter, CalculatedBill
from Area.models import Area
from UnitsRate.models import *
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime, timedelta
from decimal import Decimal
import inflect

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
        print("metere", meter)
        house = meter.house.house_number
        context = {}
        total_amount_bills = 0
        bills = CalculatedBill.objects.filter(
            meter__id=meter.id,
            bill_status='Unpaid'
        )
        last_bill = CalculatedBill.objects.filter(
            meter__id=meter.id,
            bill_status='Unpaid'
        ).last()
        fine_due_date = 0
        if last_bill:  
            for bill in bills:
                provided_date = bill.created_at.date()  # Get the date part of bill.created_at
                current_date = datetime.now().date()

                date_after_10_days = DueDateForFine.objects.all().first()
                if current_date > date_after_10_days.fine_date:
                    context['message'] = 'Do you want to include Fine ?'
                    fine_due_date += float(bill.bill_total_amount) * (float(FineAfterDueDate.objects.all().first().fine_after_due_date/100))
            context['meter'] = meter
            total_amount_bills = last_bill.bill_total_amount
        context['house'] = house
        if request.user.role == 'Meter Reader':
            context['meter'] = meter
            return render(request, 'MeterReader/meter_details.html', context)
        if request.user.role == 'Manager':
            context['meter'] = meter
            context['bills'] = bills
            context['total_amount'] = float(total_amount_bills) 
            context['fine'] = float(fine_due_date)
            return render(request, 'Manager/meter_details.html', context)
    
    def post(self,request,*args, **kwargs):
        if request.user.role == "Meter Reader":
            meter_id = kwargs.get('meter_id', None)
            bill_image = request.FILES.get('meter_img', None)
            bill_reading = request.POST.get('meter_reading', None)
            meter = Meter.objects.filter(
                id=meter_id
            ).first()
            bill = CalculatedBill.objects.filter(
                meter__id=meter_id
            ).last()
            
            bill_total_reading = int(bill_reading) -  int(bill.bill_reading) 
            print(bill_total_reading)
            bill_total_amount = 0
            first_range_of_unitValues = FirstRangeOfUnitValues.objects.all().first()
            second_range_of_unit_values = SecondtRangeOfUnitValues.objects.all().first()
            third_range_of_unit_values = ThirdRangeOfUnitValues.objects.all().first()
            fourth_range_of_unit_values = FouthRangeOfUnitValues.objects.all().first()
            if meter.house.area_type == 'commercial':
                if bill.bill_status == 'Unpaid':
                    bill_total_amount = float(bill.bill_total_amount)
                if Decimal(bill_total_reading) <=  Decimal(first_range_of_unitValues.range_of_units_commercial) and (Decimal(bill.bill_reading) < Decimal(second_range_of_unit_values.range_of_units_commercial) and Decimal(bill.bill_reading) < Decimal(third_range_of_unit_values.range_of_units_commercial)< Decimal(fourth_range_of_unit_values.range_of_units_commercial)):
                    bill_total_amount += bill_total_reading * float(first_range_of_unitValues.unit_price_for_first_range_wdcommercial)
                elif Decimal(bill_total_reading) <= Decimal(second_range_of_unit_values.range_of_units_commercial) and (Decimal(bill.bill_reading) > Decimal(first_range_of_unitValues.range_of_units_commercial) and Decimal(bill.bill_reading) < Decimal(third_range_of_unit_values.range_of_units_commercial) < Decimal(fourth_range_of_unit_values.range_of_units_commercial)):
                    bill_total_amount += bill_total_reading * float(second_range_of_unit_values.unit_price_for_second_range_wdcommercial)
                elif Decimal(bill_total_reading) <= Decimal(third_range_of_unit_values.range_of_units_commercial) and (Decimal(bill.bill_reading) > Decimal(first_range_of_unitValues.range_of_units_commercial) and Decimal(bill.bill_reading) > Decimal(second_range_of_unit_values.range_of_units_commercial) < Decimal(fourth_range_of_unit_values.range_of_units_commercial)):
                    bill_total_amount += bill_total_reading * float(third_range_of_unit_values.unit_price_for_third_range_wdcommercial)
                elif Decimal(bill_total_reading) <= Decimal(fourth_range_of_unit_values.range_of_units_commercial) and (Decimal(bill.bill_reading) > Decimal(first_range_of_unitValues.range_of_units_commercial) and Decimal(bill.bill_reading) > Decimal(second_range_of_unit_values.range_of_units_commercial) < Decimal(third_range_of_unit_values.range_of_units_commercial)):
                    bill_total_amount += bill_total_reading * float(fourth_range_of_unit_values.unit_price_for_fourth_range_wdcommercial)
                else:
                    bill_total_amount += bill_total_reading * float(fourth_range_of_unit_values.unit_price_for_fourth_range_wdcommercial)
            else:
                if bill.bill_status == 'Unpaid':
                    bill_total_amount = float(bill.bill_total_amount)
                if Decimal(bill_total_reading) <=  Decimal(first_range_of_unitValues.range_of_units_residential) and (Decimal(bill.bill_reading) < Decimal(second_range_of_unit_values.range_of_units_residential) and Decimal(bill.bill_reading) < Decimal(third_range_of_unit_values.range_of_units_residential)< Decimal(fourth_range_of_unit_values.range_of_units_residential)):
                    bill_total_amount += bill_total_reading * float(first_range_of_unitValues.unit_price_for_first_range_residentails)
                elif Decimal(bill_total_reading) <= Decimal(second_range_of_unit_values.range_of_units_residential) and (Decimal(bill.bill_reading) > Decimal(first_range_of_unitValues.range_of_units_residential) and Decimal(bill.bill_reading) < Decimal(third_range_of_unit_values.range_of_units_residential) < Decimal(fourth_range_of_unit_values.range_of_units_residential)):
                    bill_total_amount += bill_total_reading * float(second_range_of_unit_values.unit_price_for_second_range_residentails)
                elif Decimal(bill_total_reading) <= Decimal(third_range_of_unit_values.range_of_units_residential) and (Decimal(bill.bill_reading) > Decimal(first_range_of_unitValues.range_of_units_residential) and Decimal(bill.bill_reading) > Decimal(second_range_of_unit_values.range_of_units_residential) < Decimal(fourth_range_of_unit_values.range_of_units_residential)):
                    bill_total_amount += bill_total_reading * float(third_range_of_unit_values.unit_price_for_third_range_residentails)
                elif Decimal(bill_total_reading) <= Decimal(fourth_range_of_unit_values.range_of_units_residential) and (Decimal(bill.bill_reading) > Decimal(first_range_of_unitValues.range_of_units_residential) and Decimal(bill.bill_reading) > Decimal(second_range_of_unit_values.range_of_units_residential) < Decimal(third_range_of_unit_values.range_of_units_residential)):
                    bill_total_amount += bill_total_reading * float(fourth_range_of_unit_values.unit_price_for_fourht_range_residentails)
                else:
                    bill_total_amount += bill_total_reading * float(fourth_range_of_unit_values.unit_price_for_fourht_range_residentails)
            bill_total_amount += float(MiscellaneousCharges.objects.all().first().miscellaneous_charges)
            try:
                bill = CalculatedBill(
                    meter=meter,
                    bill_id=meter.meter_id,
                    bill_total_amount=bill_total_amount,
                    bill_reading_img=bill_image,
                    bill_reading=bill_reading,
                    units_consumed=bill_total_reading,
                    bill_status='Unpaid'
                )
                bill.save()
                messages.success(request, "Success")
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
            bills = CalculatedBill.objects.filter(
                meter__id=meter_id
            )
            if int(total_amount) == int(recieved_amount):
                try:
                    for bill in bills:
                        bill.bill_status = 'Paid'
                        bill.remaing_dues = 0
                        bill.save()
                    messages.success(request, "Success")
                except Exception as e:
                    print(e)
                    messages.error(request, "Error")
            else:
                pass
            return render(request, 'Manager/meter_details.html')
        return render(request, '404-error.html')
        

class GetbBill(View):
    def get(self,request,*args, **kwargs):
        meter_id = kwargs.get('meter_id', None)
       
        meter = Meter.objects.filter(
            id=meter_id
        ).first()
        area = Area.objects.filter(
            id=meter.house.id
        ).first()
        print(area)
        bills = CalculatedBill.objects.filter(
            meter__id=meter.id,
            bill_status='Unpaid'
        )
        bill_history  = CalculatedBill.objects.filter(
            meter__id=meter.id,
        )[:6]
        print(bill_history)
        last_bill = CalculatedBill.objects.filter(
            meter__id=meter.id,
            bill_status='Unpaid'
        ).last()
        context = {}
        fine_due_date = 0
        provided_date = str(last_bill.created_at)
        current_date = datetime.now().date()
        provided_datetime = datetime.strptime(provided_date, "%Y-%m-%d %H:%M:%S.%f%z")
        date_after_10_days = provided_datetime + timedelta(days=10)
        if last_bill:  
            for bill in bills:
                provided_date = str(bill.created_at)
                current_date = datetime.now().date()
                provided_datetime = datetime.strptime(provided_date, "%Y-%m-%d %H:%M:%S.%f%z")
                date_after_10_days = provided_datetime + timedelta(days=10)
                current_date_str = str(current_date)
                current_date = datetime.strptime(current_date_str, '%Y-%m-%d')
                current_date_aware = current_date.replace(tzinfo=provided_datetime.tzinfo)
                
                fine_due_date += float(bill.bill_total_amount) * (float(FineAfterDueDate.objects.all().first().fine_after_due_date/100))
            context['meter'] = meter
            total_amount_bills = last_bill.bill_total_amount
        context['history'] = bill_history
        def number_to_words(number):
            p = inflect.engine()
            return p.number_to_words(number)
        m_charges = MiscellaneousCharges.objects.all().first()
        context['last_bill'] = last_bill
        context['total_including_fine'] = float(total_amount_bills) + fine_due_date
        context['fine'] = float(FineAfterDueDate.objects.all().first().fine_after_due_date)
        context['m_charges'] = m_charges
        context['due_date'] = date_after_10_days
        context['total_amount'] = int(total_amount_bills)
        context['amount_in_words'] = number_to_words(int(total_amount_bills))
        context['area_details'] = area
        return render(request, 'index.html', context)






        







