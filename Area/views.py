from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.detail import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.http import HttpResponse
from Area.models import Area, Block
from Bills.models import Meter, CalculatedBill
from django.contrib import messages
import subprocess
from django.http import HttpResponse
from django.conf import settings
import os

class Home(View):
    def get(self,request,*args, **kwargs):
        context = {}
        areas = Area.objects.all()
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
        return redirect('/')
    
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
                area = Area(
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
                    initial_reading = CalculatedBill(
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
                    initial_reading = CalculatedBill(
                        meter=meter2,
                        bill_id=meter2.meter_id,
                        bill_total_amount=0,
                        bill_reading_img=bill_image2,
                        bill_status=bill_status2,
                        bill_reading=bill_initial_reading2
                    )
                    initial_reading.save()
                messages.success(request, 'Success')
            except Exception as e:
                print(e)
                messages.error(request, 'Error')
            if request.user.role == 'Admin':
                return render(request, 'Add_area.html')     
            elif request.user.role == 'Manager':
                return render(request, './Manager/Add_area.html')
        return render(request, '404_not_found.html')

    

class ShowAreas(View):
    def get(self, request, *args, **kwargs):
        block_name = kwargs.get('block_name', None)
        house_no =  request.GET.get('house_no')
        owner_name = request.GET.get('owner_name')
        
        context={} 
        if block_name:
            areas = Area.objects.filter(
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
            elif house_no:
                areas = areas.filter(
                    house_number__contains=house_no
                )
            elif owner_name:
                areas = areas.filter(
                    owners_name__contains=owner_name
                )
            for area in areas:
                bills = CalculatedBill.objects.filter(
                    meter__house__id=area.id
                )
                unpaid = any(bill.bill_status == 'unpaid' for bill in bills)
                paid = any( bill.bill_status =='paid' for bill in bills)
                ipaid = any(bill.bill_status == 'ipaid' for bill in bills)
                status = 'unpaid' if unpaid else ('paid' if paid else 'ipaid')
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
                area = Area.objects.filter(
                    id=area_id
                ).first()
                
                bills = CalculatedBill.objects.filter(
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
    
class GetAllReports(View):
    def get(self, request, *args, **kwargs):
        context = {}
        areas = Area.objects.all();
        all_houses = Area.objects.all().count()
        all_meters = Meter.objects.all().count()
        all_customers = Area.objects.all().count()
        reading_done = 0
        for house in areas:
            print(house.is_reading_noted())
            if house.is_reading_noted():
                reading_done += 1

        calculated_bills = CalculatedBill.objects.all()
        total_units = 0
        total_units_of_this_month = 0
        total_bill_of_this_month = 0
        total_amount_recieved = 0
        total_amount_pending = 0
        for bill in calculated_bills:
            if bill.units_consumed:
                total_units += int(bill.units_consumed) 
                total_units_of_this_month += int(bill.total_unit_of_this_month())
                total_bill_of_this_month += int(bill.total_bill_of_this_month())
                total_amount_recieved += int(bill.total_bill_recieved())
                total_amount_pending += int(bill.total_bill_pending())

        context['all_houses'] = all_houses
        context['total_bill_of_this_month'] = total_bill_of_this_month
        context['total_amount_recieved'] = total_amount_recieved
        context['total_amount_pending'] = total_amount_pending
        context['total_units'] = total_units
        context['total_units_of_this_month'] = total_units_of_this_month
        context['all_meters'] = all_meters
        context['all_customers'] = all_customers
        context['reading_done'] = reading_done
        return render(request, 'All_reports.html', context)


class CreateDump(View):
    def get(self, request, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'db.json')
        with open(file_path, 'w') as f:
            subprocess.run(['python', 'manage.py', 'dumpdata'], stdout=f)
        with open(file_path, 'rb') as f:
            file_data = f.read()
        response = HttpResponse(file_data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="db.json"'
        return response