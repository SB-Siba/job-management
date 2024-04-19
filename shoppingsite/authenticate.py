from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib import auth
from django.conf import settings
#import requests

from django.contrib.auth import logout
from helpers import privacy_t_and_c
from app_common import models


app = "shoppingsite/"


class Registration(View):
    model = models.User
    template = app + "authtemp/registration.html"

    def get(self,request):
        return render(request,self.template)
    def post(self,request):
        data = request.POST
        fullname = data.get("fullname")
        email = data.get("email")
        contact = data.get("contact")
        password = data.get("password")

        user=auth.authenticate(username=email)
        if user is None:
            try:
                new_user = self.model(full_name = fullname,email = email,contact = contact)
                new_user.set_password(password)
                new_user.save()
                messages.success(request,'Registration Successfull !!!')
                return redirect('shoppingsite:login')
            except Exception as e:
                print(e)
                messages.error(request,'Something went wrong while registering your account.\nPlease try again later.')
        return render(request,self.template)
            
class Login(View):
    model=models.User
    template = app + "authtemp/login.html"

    def get(self,request):
        return render(request,self.template)
    
    def post(self,request):
        data=request.POST
            
        user=auth.authenticate(username=data['email'], password=data['password'])

        if user is not None:      
            auth.login(request,user) 
            if user.is_superuser == True:
                return redirect('admin_dashboard:admin_dashboard') 
            else:
                return redirect('shoppingsite:home')
        else:
            messages.error(request, "Login Failed")

        return redirect('shoppingsite:login')

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('shoppingsite:login')
