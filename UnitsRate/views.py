from django.shortcuts import render
from .models import *
from django.views.generic.detail import View
from django.contrib import messages
# Create your views here.
class AddUnitCharges(View):
    
    def get(self,request,*args, **kwargs):
        commercial_unit_rates = CommercialUnitRates.objects.all().first()
        residetail_unit_rates = ResidentialUnitRates.objects.all().first()
        fine_after_due_date = FineAfterDueDate.objects.all().first()
        m_charges_ = MiscellaneousCharges.objects.all().first()
        context = {}
        context['c_unit_rates'] = commercial_unit_rates
        context['r_unit_rates'] = residetail_unit_rates     
        context['fine_after_due_date'] = fine_after_due_date
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
        commercial_unit_rates = CommercialUnitRates.objects.all().first()
        residetail_unit_rates = ResidentialUnitRates.objects.all().first()
        fine_after_due_date = FineAfterDueDate.objects.all().first()
        m_charges_ = MiscellaneousCharges.objects.all().first()
        if request.user.is_superuser or request.user.role == 'Manager':

            try:
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
                    
                messages.success(request, 'Succes')
            except Exception as e:
                print(e)
                messages.error(request, 'Error')
            return render(request, 'Add-unit-prices.html')
        else:
            return render(request, '404-error.html')
            


