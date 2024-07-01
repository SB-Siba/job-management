from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import auth
from django.conf import settings
#import requests

from django.contrib.auth import logout
from helpers import privacy_t_and_c
from . import models

app = "app_common/"

class Login(View):
    model=models.User
    template = app + "authentication/login.html"

    def get(self,request):
        return render(request,self.template)
    
    def post(self,request):
        data=request.POST

        # get_recaptcha = request.POST.get("g-recaptcha-response")
        # if not get_recaptcha:
        #     messages.error(request, 'Google Captcha Error')
        #     return redirect('app_common:login')

            
        user=auth.authenticate(username=data['email'], password=data['password'])

        if user is not None:
            
            auth.login(request,user) 
            if user.is_superuser == False:
                if user.org.is_active == False:
                    messages.error(request, 'Your Organization is Inactive. Please contact Admin.')
                    return redirect('app_common:login')

            if user.is_superuser == True:
                return redirect('admin_dashboard:admin_dashboard') 



        else: # for form validation error
            messages.error(request, "Login Failed")

        return redirect('app_common:login')

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('app_common:login')



class DeleteAccount(View):
    template = app + 'delete_account.html'
    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        messages.info(request, 'Hi we got your request, our team is working on it.')
        return redirect('app_common:delete_account')


class PrivacyPolicy(View):
    template = app + 'privacy.html'
    def get(self, request):
        context = {
            'pp': privacy_t_and_c.privacy_policy
        }
        return render(request, self.template, context)



