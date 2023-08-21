from django.shortcuts import render, redirect

# Create your views here.

from django.views.generic.detail import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import CustomUser
User = get_user_model()


class Login(View):
    def get(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home')
        return render(request, 'login.html')
    def post(self,request,*args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('/home')
        else:
            messages.error(request, 'Username or passowrd is incorrect')
            return render(request,'login.html')
        
class AddUser(View):
    def get(self,request,*args, **kwargs):
        print(request.user.role)
        return render(request, 'Add-user.html')
    
    def post(self,request,*args,**kwargs):
        user_role = request.POST.get('user_role')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        user_with_username = CustomUser.objects.filter(username=username).first()
        user_with_email = CustomUser.objects.filter(email=email).first()
        if not(user_with_email or user_with_username):
            if password == password2:
                try:
                    User.objects.create_user(email=email, username=username, password=password, role=user_role)
                    messages.success(request, 'Succes')
                except Exception as e:
                    print(e)
                    messages.error(request, 'Error')
            else:
                messages.error(request, 'Error')
        else:
            messages.error(request,'Username or email Already Exist!')
            
        return render(request, 'Add-user.html')
    

class ShowAllUsers(View):
    def get(self,request,*args, **kwargs):
        
        admin = request.GET.get('admin', None)
        manager = request.GET.get('manager', None)
        m_reader = request.GET.get('m_reader', None)
        print(admin, manager, m_reader)
        users = CustomUser.objects.all()
        if admin:
            users = users.filter(
            role='Admin'
            )
        elif manager:
            users = users.filter(
            role='Manager'
            )
        elif m_reader:
            users = users.filter(
            role='Meter Reader'
            )
        context = {}
        context['users'] = users

        return render(request, 'user_list.html', context)


    
    


