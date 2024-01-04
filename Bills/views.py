from django.shortcuts import render
from .models import Meter, CalculatedBill
from Area.models import Area
from UnitsRate.models import *
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime, timedelta,timezone
from decimal import Decimal
import inflect
from django.http import HttpResponse
from django.template.loader import get_template

from io import BytesIO
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
        total_amount_bills = 0
        bills = CalculatedBill.objects.filter(
            meter__id=meter.id,
            bill_status='unpaid'
        )
        last_bill = CalculatedBill.objects.filter(
            meter__id=meter.id,
            bill_status='unpaid'
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
            bill = CalculatedBill.objects.filter(meter__id=meter.id).first()
            area = Area.objects.filter(
                id=meter.house.id
            ).first()
            context['area'] = area

            return render(request, 'MeterReader/meter_details.html', context)
        if request.user.role == 'Manager':
            context['meter'] = meter
            context['bills'] = bills
            context['total_amount'] = float(total_amount_bills) 
            context['fine'] = float(fine_due_date)
            return render(request, 'Manager/meter_details.html', context)
    
    def post(self,request,*args, **kwargs):
        if request.user.role == "Meter Reader":
            bill_total_amount = 0
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
            first_range_of_unitValues = FirstRangeOfUnitValue.objects.all().first()
            second_range_of_unit_values = SecondRangeOfUnitValue.objects.all().first()
            third_range_of_unit_values = ThirdRangeOfUnitValue.objects.all().first()
            fourth_range_of_unit_values = FouthRangeOfUnitValue.objects.all().first()
            if meter.house.area_type == 'commercial':
                if bill.bill_status == 'unpaid':
                    bill_total_amount = float(bill.bill_total_amount)
                if bill.bill_status == 'ipaid':
                    bill_total_amount += float(bill.remaing_dues)
                    print("Before",bill_total_amount)
                print("After",bill_total_amount)
                if Decimal(bill_total_reading) <=  Decimal(first_range_of_unitValues.range_of_units_commercial) and (Decimal(bill_total_reading) < Decimal(second_range_of_unit_values.range_of_units_commercial) and Decimal(bill_total_reading) < Decimal(third_range_of_unit_values.range_of_units_commercial) and Decimal(bill_total_reading) < Decimal(fourth_range_of_unit_values.range_of_units_commercial)):
                    bill_total_amount += bill_total_reading * float(first_range_of_unitValues.unit_price_for_first_range_wdcommercial)
                elif Decimal(bill_total_reading) <= Decimal(second_range_of_unit_values.range_of_units_commercial) and (Decimal(bill_total_reading) > Decimal(first_range_of_unitValues.range_of_units_commercial) and Decimal(bill_total_reading) < Decimal(third_range_of_unit_values.range_of_units_commercial) and Decimal(bill_total_reading) < Decimal(fourth_range_of_unit_values.range_of_units_commercial)):
                    bill_total_amount += bill_total_reading * float(second_range_of_unit_values.unit_price_for_second_range_wdcommercial)
                elif Decimal(bill_total_reading) <= Decimal(third_range_of_unit_values.range_of_units_commercial) and (Decimal(bill_total_reading) > Decimal(first_range_of_unitValues.range_of_units_commercial) and Decimal(bill_total_reading) > Decimal(second_range_of_unit_values.range_of_units_commercial) and Decimal(bill_total_reading) < Decimal(fourth_range_of_unit_values.range_of_units_commercial)):
                    bill_total_amount += bill_total_reading * float(third_range_of_unit_values.unit_price_for_third_range_wdcommercial)
                elif Decimal(bill_total_reading) <= Decimal(fourth_range_of_unit_values.range_of_units_commercial) and (Decimal(bill_total_reading) > Decimal(first_range_of_unitValues.range_of_units_commercial) and Decimal(bill_total_reading) > Decimal(second_range_of_unit_values.range_of_units_commercial) and Decimal(bill_total_reading) > Decimal(third_range_of_unit_values.range_of_units_commercial)):
                    bill_total_amount += bill_total_reading * float(fourth_range_of_unit_values.unit_price_for_fourth_range_wdcommercial)
                else:
                    bill_total_amount += bill_total_reading * float(fourth_range_of_unit_values.unit_price_for_fourth_range_wdcommercial)
                    
            else:
                if bill.bill_status == 'unpaid':
                    bill_total_amount = float(bill.bill_total_amount)
                if bill.bill_status == 'ipaid':
                    bill_total_amount += float(bill.remaing_dues)
                if Decimal(bill_total_reading) <=  Decimal(first_range_of_unitValues.range_of_units_residential) and (Decimal(bill_total_reading) < Decimal(second_range_of_unit_values.range_of_units_residential) and Decimal(bill_total_reading) < Decimal(third_range_of_unit_values.range_of_units_residential) and Decimal(bill_total_reading) < Decimal(fourth_range_of_unit_values.range_of_units_residential)):
                    bill_total_amount += bill_total_reading * float(first_range_of_unitValues.unit_price_for_first_range_residentails)
                elif Decimal(bill_total_reading) <= Decimal(second_range_of_unit_values.range_of_units_residential) and (Decimal(bill_total_reading) > Decimal(first_range_of_unitValues.range_of_units_residential) and Decimal(bill_total_reading) < Decimal(third_range_of_unit_values.range_of_units_residential) and Decimal(bill_total_reading) < Decimal(fourth_range_of_unit_values.range_of_units_residential)):
                    bill_total_amount += bill_total_reading * float(second_range_of_unit_values.unit_price_for_second_range_residentails)
                elif Decimal(bill_total_reading) <= Decimal(third_range_of_unit_values.range_of_units_residential) and (Decimal(bill_total_reading) > Decimal(first_range_of_unitValues.range_of_units_residential) and Decimal(bill_total_reading) > Decimal(second_range_of_unit_values.range_of_units_residential) and Decimal(bill_total_reading) < Decimal(fourth_range_of_unit_values.range_of_units_residential)):
                    bill_total_amount += bill_total_reading * float(third_range_of_unit_values.unit_price_for_third_range_residentails)
                elif Decimal(bill_total_reading) <= Decimal(fourth_range_of_unit_values.range_of_units_residential) and (Decimal(bill_total_reading) > Decimal(first_range_of_unitValues.range_of_units_residential) and Decimal(bill_total_reading) > Decimal(second_range_of_unit_values.range_of_units_residential) and Decimal(bill_total_reading) > Decimal(third_range_of_unit_values.range_of_units_residential)):
                    bill_total_amount += bill_total_reading * float(fourth_range_of_unit_values.unit_price_for_fourht_range_residentails)
                else:
                    bill_total_amount += bill_total_reading * float(fourth_range_of_unit_values.unit_price_for_fourht_range_residentails)
            bill_total_amount += float(MiscellaneousCharges.objects.all().first().miscellaneous_charges)
            try:
                pkt_offset = timedelta(hours=5)
                pkt = timezone(pkt_offset)
                now_utc = datetime.now(timezone.utc)
                now_pkt = now_utc.astimezone(pkt)
                print("NOw Pkt", now_pkt)
                bill = CalculatedBill(
                    meter=meter,
                    bill_id=meter.meter_id,
                    bill_total_amount=bill_total_amount,
                    bill_reading_img=bill_image,
                    bill_reading=bill_reading,
                    units_consumed=bill_total_reading,
                    bill_status='unpaid',
                )
                print(bill.created_at)
                bill.save()
                messages.success(request, "Success")
            except Exception as e:
                messages.error(request, 'Error')
            print(meter_id)
            return render(request, 'MeterReader/meter_details.html')
        elif request.user.role == 'Manager':
            meter_id = kwargs.get('meter_id', None)
            total_amount = float(request.POST.get('total_amount', None))
            recieved_amount = float(request.POST.get('r_amount', None))
            remaining_dues = total_amount - recieved_amount
            print(remaining_dues)
            bills = list(CalculatedBill.objects.filter(
                meter__id=meter_id,
                bill_status='unpaid'
            ))
            print(bills)
            
            try:
                if remaining_dues == 0:
                    for bill in bills:
                        bill.bill_status = 'paid'
                        bill.remaing_dues = 0
                        bill.payment_recieved = recieved_amount
                        bill.save()
                        bills.pop(-1)
                elif remaining_dues > 0:
                    bills[-1].remaing_dues = remaining_dues
                    bills[-1].bill_status = 'ipaid'
                    bills[-1].payment_recieved = recieved_amount
                    bills[-1].save()
                if len(bills) > 1:
                    for bill in bills[:-1]:
                        bill.bill_status = 'paid'
                        bill.remaing_dues = 0
                        bill.payment_recieved = recieved_amount
                        bill.save()
                messages.success(request, "Success")    
            except Exception as e:
                print(e)
                messages.error(request, "Error")
            
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
            bill_status='unpaid'
        )
        bill_history  = CalculatedBill.objects.filter(
            meter__id=meter.id,
        )[:6]
        print(bill_history)
        last_bill = CalculatedBill.objects.filter(
            meter__id=meter.id,
            bill_status='unpaid'
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
                context['current_date'] = current_date
                fine_due_date += float(bill.bill_total_amount) * (float(FineAfterDueDate.objects.all().first().fine_after_due_date/100))
            context['meter'] = meter
            total_amount_bills = last_bill.bill_total_amount
        context['history'] = bill_history
        def number_to_words(number):
            p = inflect.engine()
            return p.number_to_words(number)
        last_item_index = len(bill_history) - 2
        last_item = bill_history[last_item_index] if last_item_index >= 0 else None 
        context['lastitem'] = last_item
        m_charges = MiscellaneousCharges.objects.all().first()
        context['last_bill'] = last_bill
        context['total_including_fine'] = float(total_amount_bills) + fine_due_date
        context['fine'] = float(FineAfterDueDate.objects.all().first().fine_after_due_date)
        context['m_charges'] = m_charges
        context['due_date'] = date_after_10_days
        
        context['total_bill_without_MSC'] = int(total_amount_bills) - float(MiscellaneousCharges.objects.all().first().miscellaneous_charges)
        context['total_amount'] = int(total_amount_bills)
        context['amount_in_words'] = number_to_words(int(total_amount_bills))
        context['area_details'] = area
        return render(request, 'index.html', context)
