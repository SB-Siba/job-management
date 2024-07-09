from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.conf import settings
#import requests
from django.http import JsonResponse
import json
from django.contrib.auth.hashers import make_password
from helpers import utils

from . import form
from app_common import models as common_model


app = "admin_dashboard/credentials/"

# ================================================== credential management ==========================================

@method_decorator(utils.super_admin_only, name='dispatch')
class CreateCredential(View):
    model = common_model.User
    form_class = form.UserCreateForm
    template = app + "add_credential.html"

    def get(self,request):
        user_list = self.model.objects.filter(is_superuser = False).order_by('-id')
        context = {
            "form": self.form_class,
            "user_list" : user_list
        }
        return render(request, self.template, context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit= True)
            obj.password = make_password(request.POST.get("password"))
            obj.save()
            messages.success(request, f"Credential of username: {request.POST.get('email')} is created successfully")
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return redirect("admin_dashboard:add_credential")



@method_decorator(utils.super_admin_only, name='dispatch')
class Change_password(View):
    model = common_model.User

    def post(self,request):
        
        user = self.model.objects.get(id = request.POST.get("user_id"))
        user.password = make_password(request.POST.get("password"))
        user.save()
        messages.success(request, f"Password of {user.email} is changed to {request.POST.get('password')}")
        return redirect("admin_dashboard:add_credential")


@method_decorator(utils.super_admin_only, name='dispatch')
class UserActiveInactive(View):
    model = common_model.User

    def get(self,request):
        user_id = request.GET.get("user_id")
        user = self.model.objects.get(id = user_id)

        user_status = ''

        if user.is_active == True:
            user.is_active = False
            user_status = False
            
        else:
            user.is_active = True
            user_status = True

        user.save()
        
        return JsonResponse(user_status, safe=False)
