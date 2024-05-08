from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib import auth
from django.conf import settings
#import requests
from .forms import SignUpForm,LoginForm
from django.contrib.auth import logout
from helpers import privacy_t_and_c
from app_common import models


app = "shoppingsite/"


class Registration(View):
    model = models.User
    template = app + "authtemp/registration.html"

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            full_name = form.cleaned_data.get('full_name')

            user = auth.authenticate(request, username=email, password=password)
            if user is None:
                try:
                    if password == confirm_password:
                        new_user = self.model(email=email, full_name=full_name)
                        new_user.set_password(password)
                        new_user.save()
                        messages.success(request, 'Registration Successful!')
                        return redirect('shoppingsite:login')
                    else:
                        messages.error(request, "Password does not match with Confirm Password")
                        return redirect('shoppingsite:signup')
                except Exception as e:
                    print(e)
                    messages.error(request, 'Something went wrong while registering your account. Please try again later.')
            else:
                messages.error(request, "User already exists.")
        return render(request, self.template, {'form': form})
            
class Login(View):
    model=models.User
    template = app + "authtemp/login.html"

    def get(self,request):
        form = LoginForm()
        return render(request, self.template, {'form': form})
    
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            user=auth.authenticate(username=email, password=password)

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
