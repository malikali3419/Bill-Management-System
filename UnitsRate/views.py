from django.shortcuts import render
from .models import *
from django.views.generic.detail import View
from django.contrib import messages
from decimal import Decimal
# Create your views here.
from datetime import datetime
class AddUnitCharges(View):
    
    def get(self,request,*args, **kwargs):
        commercial_unit_rates = CommercialUnitRates.objects.all().first()
        residetail_unit_rates = ResidentialUnitRates.objects.all().first()
        fine_after_due_date = FineAfterDueDate.objects.all().first()
        m_charges_ = MiscellaneousCharges.objects.all().first()
        first_range_of_unitValues = FirstRangeOfUnitValues.objects.all().first()
        second_range_of_unit_values = SecondtRangeOfUnitValues.objects.all().first()
        third_range_of_unit_values = ThirdRangeOfUnitValues.objects.all().first()
        fourth_range_of_unit_values = FouthRangeOfUnitValues.objects.all().first()
        fine_due_date = DueDateForFine.objects.all().first()
        fine_due_date = fine_due_date.fine_date
        formatted_fine_due_date = fine_due_date.strftime('%Y-%m-%d')
        context = {}
        context['c_unit_rates'] = commercial_unit_rates
        context['r_unit_rates'] = residetail_unit_rates     
        context['fine_after_due_date'] = fine_after_due_date
        context['first_range_of_unitValues'] = first_range_of_unitValues
        context['second_range_of_unit_values'] = second_range_of_unit_values
        context['third_range_of_unit_values'] = third_range_of_unit_values
        context['fourth_range_of_unit_values'] = fourth_range_of_unit_values
        context['fine_due_date'] = formatted_fine_due_date
        context['m_charges'] = m_charges_
        if request.user.is_superuser:
            return render(request, 'Add-unit-prices.html', context)
        if request.user.role == 'Manager':
            return render(request, 'Manager/Add-unit-prices.html',context)

    def post(self, request, *args, **kwargs):
        c_unit_price = request.POST.get('c_unit_price', None)
        r_unit_price = request.POST.get('r_unit_peices', None)
        fine_after_due = request.POST.get('fine', None)
        m_charges = request.POST.get('m_charges', None)
        fine_date = request.POST.get('fine_date', None)
        first_range_input_r =  Decimal(request.POST.get('first_range_input_r', None))
        second_range_input_r =  Decimal(request.POST.get('second_range_input_r', None))
        third_range_input_r =  Decimal(request.POST.get('third_range_input_r', None))
        fourth_range_input_r = Decimal(request.POST.get('fourth_range_input_r'),None)
        first_range_unit_charges_r =  Decimal(request.POST.get('first_range_unit_charges_r', None))
        second_range_unit_charges_r =  Decimal(request.POST.get('second_range_unit_charges_r', None))
        third_range_unit_charges_r =  Decimal(request.POST.get('third_range_unit_charges_r', None))
        fourth_range_unit_charges_r = Decimal(request.POST.get('fourth_range_unit_charges_r'),None)
        first_range_input_c =  Decimal(request.POST.get('first_range_input_c', None))
        second_range_input_c =  Decimal(request.POST.get('second_range_input_c', None))
        third_range_input_c =  Decimal(request.POST.get('third_range_input_c', None))
        fourth_range_input_c = Decimal(request.POST.get('fourth_range_input_c'),None)
        first_range_unit_charges_c =  Decimal(request.POST.get('first_range_unit_charges_c', None))
        second_range_unit_charges_c =  Decimal(request.POST.get('second_range_unit_charges_c', None))
        third_range_unit_charges_c =  Decimal(request.POST.get('third_range_unit_charges_c', None))
        fourth_range_unit_charges_c = Decimal(request.POST.get('fourth_range_unit_charges_c'),None)
        first_range_of_unitValues = FirstRangeOfUnitValues.objects.all()
        second_range_of_unit_values = SecondtRangeOfUnitValues.objects.all()
        third_range_of_unit_values = ThirdRangeOfUnitValues.objects.all()
        fourth_range_of_unit_values = FouthRangeOfUnitValues.objects.all()
        commercial_unit_rates = CommercialUnitRates.objects.all().first()
        residetail_unit_rates = ResidentialUnitRates.objects.all().first()
        fine_after_due_date = FineAfterDueDate.objects.all().first()
        m_charges_ = MiscellaneousCharges.objects.all().first()
        due_date_model = DueDateForFine.objects.all().first()
        if request.user.is_superuser or request.user.role == 'Admin' or request.user.role == 'Manager':
            try:
                if first_range_of_unitValues:
                    first_input_range = FirstRangeOfUnitValues.objects.all().first()
                    first_input_range.range_of_units_residential = first_range_input_r
                    first_input_range.unit_price_for_first_range_residentails =  first_range_unit_charges_r
                    first_input_range.range_of_units_commercial = first_range_input_c
                    first_input_range.unit_price_for_first_range_wdcommercial =first_range_unit_charges_c
                    first_input_range.save()
                    
                else:
                    first_input_range = FirstRangeOfUnitValues(
                        range_of_units_residential= first_range_input_r,
                        unit_price_for_first_range_residentails=first_range_unit_charges_r,
                        range_of_units_commercial=first_range_input_c,
                        unit_price_for_first_range_wdcommercial=first_range_unit_charges_c
                    )
                    first_input_range.save()
                if second_range_of_unit_values:
                    second_range_unit_values = SecondtRangeOfUnitValues.objects.all().first()
                    second_range_unit_values.range_of_units_residential = second_range_input_r
                    second_range_unit_values.unit_price_for_second_range_residentails = second_range_unit_charges_r
                    second_range_unit_values.range_of_units_commercial = second_range_input_c
                    second_range_unit_values.unit_price_for_second_range_wdcommercial = second_range_unit_charges_c
                    second_range_unit_values.save()
                else:
                    second_range_unit_values = SecondtRangeOfUnitValues(
                        range_of_units_residential= second_range_input_r,
                        unit_price_for_second_range_residentails=second_range_unit_charges_r,
                        range_of_units_commercial=second_range_input_c,
                        unit_price_for_second_range_wdcommercial=second_range_unit_charges_c
                    )
                    second_range_unit_values.save()
                if third_range_of_unit_values:
                    third_range_input_values = ThirdRangeOfUnitValues.objects.all().first()
                    third_range_input_values.range_of_units_residential = third_range_input_r
                    third_range_input_values.unit_price_for_third_range_residentails = third_range_unit_charges_r
                    third_range_input_values.range_of_units_commercial = third_range_input_c
                    third_range_input_values.unit_price_for_third_range_wdcommercial = third_range_unit_charges_c
                    third_range_input_values.save()
                else:
                    third_range_input_values = ThirdRangeOfUnitValues(
                        range_of_units_residential= third_range_input_r,
                        unit_price_for_third_range_residentails=third_range_unit_charges_r,
                        range_of_units_commercial=third_range_input_c,
                        unit_price_for_third_range_wdcommercial=third_range_unit_charges_c
                    )
                    third_range_input_values.save()
                if fourth_range_of_unit_values:
                    fourth_range_unit_values = FouthRangeOfUnitValues.objects.all().first()
                    fourth_range_unit_values.range_of_units_residential = fourth_range_input_r
                    fourth_range_unit_values.unit_price_for_fourht_range_residentails = fourth_range_unit_charges_r
                    fourth_range_unit_values.range_of_units_commercial = fourth_range_input_c
                    fourth_range_unit_values.unit_price_for_fourth_range_wdcommercial = fourth_range_unit_charges_c
                    fourth_range_unit_values.save()
                else:
                    fourth_range_unit_values = FouthRangeOfUnitValues(
                        range_of_units_residential= fourth_range_input_r,
                        unit_price_for_fourht_range_residentails=fourth_range_unit_charges_r,
                        range_of_units_commercial=fourth_range_input_c,
                        unit_price_for_fourth_range_wdcommercial=fourth_range_unit_charges_c
                    )
                    fourth_range_unit_values.save()
                if commercial_unit_rates:
                    new_c_unit_price = CommercialUnitRates.objects.all().first()
                    new_c_unit_price.commercial_unit_price = c_unit_price
                    new_c_unit_price.save()
                else:
                    new_c_unit_price = CommercialUnitRates.objects.create(
                        commercial_unit_price=c_unit_price
                    )
                    new_c_unit_price.save()
                if residetail_unit_rates:
                    new_r_unit_price = ResidentialUnitRates.objects.all().first()
                    new_r_unit_price.residential_unit_price = r_unit_price
                    new_r_unit_price.save()
                else:
                    new_r_unit_price = ResidentialUnitRates.objects.create(
                        residential_unit_price=r_unit_price
                    )
                    new_r_unit_price.save()
                if fine_after_due_date:
                    new_fine_rate = FineAfterDueDate.objects.all().first()
                    new_fine_rate.fine_after_due_date = fine_after_due
                    new_fine_rate.save()
                else:
                    new_fine_rate = FineAfterDueDate.objects.create(
                        fine_after_due_date=fine_after_due
                    )
                    
                if m_charges_:
                    new_m_charges = MiscellaneousCharges.objects.all().first()
                    new_m_charges.miscellaneous_charges = m_charges
                    new_m_charges.save()
                else:
                    new_m_charges = MiscellaneousCharges.objects.create(
                        miscellaneous_charges=m_charges
                    )
                if due_date_model:
                    fine_date_ = DueDateForFine.objects.all().first()
                    fine_date_.fine_date= fine_date
                    fine_date_.save()
                else:
                    new_fine_date = DueDateForFine.objects.create(
                        fine_date=fine_date
                    )
                    
                messages.success(request, 'Success')
            except Exception as e:
                print(e)
                messages.error(request, 'Error')
            if request.user.role == 'Manager':
                return render(request, './Manager/Add-unit-prices.html')
            elif request.user.role == 'Admin':
                return render(request, 'Add-unit-prices.html')
        else:
            return render(request, '404-error.html')
            


