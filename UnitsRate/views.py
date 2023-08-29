from django.shortcuts import render
from .models import *
from django.views.generic.detail import View
from django.contrib import messages
from decimal import Decimal
# Create your views here.
class AddUnitCharges(View):
    
    def get(self,request,*args, **kwargs):
        commercial_unit_rates = CommercialUnitRates.objects.all().first()
        residetail_unit_rates = ResidentialUnitRates.objects.all().first()
        fine_after_due_date = FineAfterDueDate.objects.all().first()
        m_charges_ = MiscellaneousCharges.objects.all().first()
        unit_value_less_than_200_model = UnitValues200OrLess.objects.all().first()
        unit_value_less_than_400_model = UnitValues400OrLess.objects.all().first()
        unit_value_less_than_600_model = UnitValues600OrLess.objects.all().first()
        context = {}
        context['c_unit_rates'] = commercial_unit_rates
        context['r_unit_rates'] = residetail_unit_rates     
        context['fine_after_due_date'] = fine_after_due_date
        context['unit_or_range_values_less_than_200'] = unit_value_less_than_200_model
        context['unit_or_range_values_less_than_400'] = unit_value_less_than_400_model
        context['unit_or_range_values_less_than_600'] = unit_value_less_than_600_model

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
        input_range_less_than_200_r =  Decimal(request.POST.get('200_input_range_r', None))
        input_range_less_than_400_r =  Decimal(request.POST.get('400_input_range_r', None))
        input_range_less_than_600_r =  Decimal(request.POST.get('600_input_range_r', None))
        unit_price_less_than_200_r =  Decimal(request.POST.get('200_unit_price_r', None))
        unit_price_less_than_400_r =  Decimal(request.POST.get('400_unit_price_r', None))
        unit_price_less_than_600_r =  Decimal(request.POST.get('600_unit_price_r', None))
        input_range_less_than_200_c =  Decimal(request.POST.get('200_input_range_c', None))
        input_range_less_than_400_c =  Decimal(request.POST.get('400_input_range_c', None))
        input_range_less_than_600_c =  Decimal(request.POST.get('600_input_range_c', None))
        unit_price_less_than_200_c =  Decimal(request.POST.get('200_unit_price_c', None))
        unit_price_less_than_400_c =  Decimal(request.POST.get('400_unit_price_c', None))
        unit_price_less_than_600_c =  Decimal(request.POST.get('600_unit_price_c', None))
        unit_value_less_than_200_model = UnitValues200OrLess.objects.all()
        unit_value_less_than_400_model = UnitValues400OrLess.objects.all()
        unit_value_less_than_600_model = UnitValues600OrLess.objects.all()
        commercial_unit_rates = CommercialUnitRates.objects.all().first()
        residetail_unit_rates = ResidentialUnitRates.objects.all().first()
        fine_after_due_date = FineAfterDueDate.objects.all().first()
        m_charges_ = MiscellaneousCharges.objects.all().first()
        if request.user.is_superuser or request.user.role == 'Manager':

            try:
                if unit_value_less_than_200_model:
                    print(type(input_range_less_than_200_r), type(unit_price_less_than_200_r), type(input_range_less_than_200_c), type(unit_price_less_than_200_c))
                    new_unit_values_for_200_or_less = UnitValues200OrLess.objects.all().first()
                    new_unit_values_for_200_or_less.range_for_200_or_less_residential = input_range_less_than_200_r
                    new_unit_values_for_200_or_less.unit_price_for_200_less_units_residentails =  unit_price_less_than_200_r
                    new_unit_values_for_200_or_less.range_for_200_or_less_commercial = input_range_less_than_200_c
                    new_unit_values_for_200_or_less.unit_price_for_200_less_units_commercial =unit_price_less_than_200_c
                    new_unit_values_for_200_or_less.save()
                    
                else:
                    new_unit_values_for_200_or_less = UnitValues200OrLess(
                        range_for_200_or_less_residential= input_range_less_than_200_r,
                        unit_price_for_200_less_units_residentails=unit_price_less_than_200_r,
                        range_for_200_or_less_commercial=input_range_less_than_200_c,
                        unit_price_for_200_less_units_commercial=unit_price_less_than_200_c
                    )
                    new_unit_values_for_200_or_less.save()
                if unit_value_less_than_400_model:
                    new_unit_values_for_400_or_less = UnitValues400OrLess.objects.all().first()
                    new_unit_values_for_400_or_less.range_for_400_or_less_residentials = input_range_less_than_400_r
                    new_unit_values_for_400_or_less.unit_price_for_400_less_units_residentials = unit_price_less_than_400_r
                    new_unit_values_for_400_or_less.range_for_400_or_less_commercial = input_range_less_than_400_c
                    new_unit_values_for_400_or_less.unit_price_for_400_less_units_commercial = unit_price_less_than_400_c
                    new_unit_values_for_400_or_less.save()
                else:
                    new_unit_values_for_400_or_less = UnitValues400OrLess(
                        range_for_400_or_less_residentials= input_range_less_than_400_r,
                        unit_price_for_400_less_units_residentials=unit_price_less_than_400_r,
                        range_for_400_or_less_commercial=input_range_less_than_400_c,
                        unit_price_for_400_less_units_commercial=unit_price_less_than_400_c
                    )
                    new_unit_values_for_400_or_less.save()
                if unit_value_less_than_600_model:
                    new_unit_values_for_600_or_less = UnitValues600OrLess.objects.all().first()
                    new_unit_values_for_400_or_less.range_for_600_or_less_residentials = input_range_less_than_600_r
                    new_unit_values_for_600_or_less.unit_price_for_600_less_units_residentials = unit_price_less_than_600_r
                    new_unit_values_for_600_or_less.range_for_600_or_less_commercial = input_range_less_than_600_c
                    new_unit_values_for_600_or_less.unit_price_for_600_less_units_commercial = unit_price_less_than_600_c
                    new_unit_values_for_600_or_less.save()
                else:
                    new_unit_values_for_600_or_less = UnitValues600OrLess(
                        range_for_600_or_less_residentials= input_range_less_than_600_r,
                        unit_price_for_600_less_units_residentials=unit_price_less_than_600_r,
                        range_for_600_or_less_commercial=input_range_less_than_600_c,
                        unit_price_for_600_less_units_commercial=unit_price_less_than_600_c
                    )
                    new_unit_values_for_600_or_less.save()
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
                    
                messages.success(request, 'Success')
            except Exception as e:
                print(e)
                messages.error(request, 'Error')
            return render(request, 'Add-unit-prices.html')
        else:
            return render(request, '404-error.html')
            


