from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.detail import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.http import HttpResponse
from Area.models import Areas, Block
from Bills.models import Meter, CalculatedBills
from django.contrib import messages

class Home(View):
    def get(self,request,*args, **kwargs):
        context = {}
        areas = Areas.objects.all()
        bill = Meter.objects.all()
        context['areas'] = areas
        blocks = Block.objects.all()
        context['blocks'] = blocks
        if not request.user.is_authenticated:
            return redirect('/User/login')
        if request.user.is_superuser or request.user.role == 'Admin':
            return render(request, 'admin-home-blocks.html', context)
        if request.user.role == 'Meter Reader':
            return render(request, './MeterReader/home-meter-reader.html',context)
        if request.user.role == 'Manager':
            return render(request, 'Manager/manager-home-blocks.html', context)

        return render(request, '404_not_found.html')
    
    def post(self,request,*args, **kwargs):
        if 'block_name' in request.POST:
            block_name = request.POST.get('block_name', None)
            block = Block(
                block_name=block_name
            )
            block.save()
        return redirect('/home')
    
class AddHouse(View):
    def get(self,request,*args, **kwargs):
        blocks = Block.objects.all()
        context = {}
        context['blocks'] = blocks
        if request.user.role == 'Admin' or request.user.is_superuser:
            return render(request, 'Add_area.html',context)
        if request.user.role == 'Manager':
            return render(request, 'Manager/Add_area.html', context)

        return render(request, '404_not_found.html')

    
    def post(self,request,*args, **kwargs):
        if request.user.role == 'Admin' or request.user.is_superuser or request.user.role == 'Manager':
            area_type = request.POST.get('area_type', None)
            area_no = request.POST.get('area_no', None)
            area_owner_name =request.POST.get('owner_name', None)
            owner_cnic = request.POST.get('cnic', None)
            owner_phone_number = request.POST.get('phone_number', None)
            area_block = request.POST.get('area_block', None)
            meter_id = request.POST.get('bill_no', None)
            meter_owner = request.POST.get('bill_owner', None)
            meter_type = request.POST.get('bill_type', None)
            bill_image = request.FILES.get('bill_img', None)
            bill_status = request.POST.get('bill_status', None)
            bill_initial_reading = request.POST.get('bill_reading', None)
            meter_id2 = request.POST.get('bill_id2', None)
            meter_owner2 = request.POST.get('bill_owner2', None)
            meter_type2 = request.POST.get('bill_type2', None)
            bill_image2 = request.FILES.get('bill_img2', None)
            bill_status2 = request.POST.get('bill_status2', None)
            bill_initial_reading2 = request.POST.get('bill_reading2', None)
            print(meter_id)
            try:
                area = Areas(
                owners_name=area_owner_name,
                CNIC=owner_cnic,
                house_number=area_no,
                area_block=area_block,
                area_type = area_type,
                owners_phone_number=owner_phone_number
                )
                area.save()
                if meter_id:
                    meter = Meter(
                        house=area,
                        meter_id=meter_id,
                        meter_owner=meter_owner,
                        meter_type = meter_type,
                    )
                    meter.save()
                    initial_reading = CalculatedBills(
                        meter=meter,
                        bill_id=meter.meter_id,
                        bill_total_amount=0,
                        bill_reading_img=bill_image,
                        bill_status=bill_status,
                        bill_reading=bill_initial_reading
                    )
                    initial_reading.save()
                if meter_id2:
                    meter2 = Meter(
                        house=area,
                        meter_id=meter_id2,
                        meter_owner=meter_owner2,
                        meter_type=meter_type2,
                    )
                    meter2.save()
                    initial_reading = CalculatedBills(
                        meter=meter2,
                        bill_id=meter2.meter_id,
                        bill_total_amount=0,
                        bill_reading_img=bill_image2,
                        bill_status=bill_status2,
                        bill_reading=bill_initial_reading2
                    )
                    initial_reading.save()
                messages.success(request, 'Succes')
            except Exception as e:
                print(e)
                messages.error(request, 'Error')
            return render(request, 'Add_area.html')     
        return render(request, '404_not_found.html')

    

class ShowAreas(View):
    def get(self, request, *args, **kwargs):
        block_name = kwargs.get('block_name', None) 
        
        context={} 
        if block_name:
            areas = Areas.objects.filter(
                area_block=block_name 
            )
            residential = request.GET.get('residential', None)
            commercial = request.GET.get('commercial', None)
            if residential:
                areas = areas.filter(
                    area_type='residential'
                )
            elif commercial:
                areas = areas.filter(
                    area_type='commercial'
                )
            for area in areas:
                bills = CalculatedBills.objects.filter(
                    meter__house__id=area.id
                )
                unpaid = any(bill.bill_status == 'Unpaid' for bill in bills)
                status = 'unpaid' if unpaid else 'paid'
                area.bill_paid_status = status
                area.save()
            context['areas'] = areas
        if request.user.role == 'Meter Reader':
            return render(request, "MeterReader/areas-home-reader.html", context)
        if request.user.role == 'Manager':
            return render(request, "Manager/areas-home-manager.html", context)
        return render(request, 'admin-home.html', context)
    
class ShowAreaDetails(View):
    def get(self, request, *args, **kwargs):
        if request.user.role == 'Admin' or request.user.is_superuser or request.user.role == 'Manager':
            area_id = kwargs.get('area_id', None)
            context={} 
            if area_id:
                area = Areas.objects.filter(
                    id=area_id
                ).first()
                
                bills = CalculatedBills.objects.filter(
                    meter__house__id=area_id
                )
           
            context['area'] = area
            context['bills'] = bills
            if request.user.role == 'Meter Reader':
                context['user_role'] = 'M_reader'
            
            return render(request, 'Area-details.html', context)
        return render(request, '404_not_found.html')

class Logout(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return redirect ('/User/login')
    
