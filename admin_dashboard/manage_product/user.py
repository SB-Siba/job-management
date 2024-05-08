from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from helpers import utils, api_permission
from django.contrib import messages
from shoppingsite import forms as siteforms
from admin_dashboard.manage_product import forms
import os
from app_common import models as common_model

app = "admin_dashboard/users/"

class UserList(View):
    model = common_model.User
    template = app + "user_list.html"

    def get(self,request):
        user_obj = self.model.objects.filter(is_superuser=False).order_by("id")
        return render(request,self.template,{"user_obj":user_obj})
    
def delete_user(request,id=None):
    user = common_model.User.objects.filter(pk=id).first()
    if not user:
        messages.error(request,"The selected user does not exist.")
        return redirect('admin_dashboard:userslist')
    else:
       user.delete()
       messages.success(request,"Successfully deleted the user!")
       return redirect('admin_dashboard:userslist') 