from django.shortcuts import render, redirect , HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from helpers import utils, api_permission
from django.contrib import messages
from user import forms as siteforms
from admin_dashboard.manage_product import forms
import os
from app_common import models as common_model
from user import forms

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

def user_detail(request,id=None):
    user_detail =  common_model.UserProfile.objects.filter(pk=id).first()
    # return render(request,self.user:profile,{"user_obj":user_obj})
    return redirect('user:profile')
# views.py
# from django.shortcuts import get_object_or_404
# from django.http import JsonResponse


# def user_detail(request, user_id):
#         user = get_object_or_404(User, id=user_id)
#         data = {
#             'id': User.id,
#             'username': User.username,
#             'email': User.email,
#             'first_name': User.first_name,
#             'last_name': User.last_name,
#     }
#         return JsonResponse(data)

def Edit_User(request,user_id):
    request.session['user_id'] = user_id
    user = User.objects.get(admin = user_id)
    form = EditUserForm()
    form.fields['email'].initial = user.admin.email
    form.fields['first_name'].initial = user.admin.first_name
    form.fields['last_name'].initial = user.admin.last_name
    form.fields['contact'].initial = user.admin.contact


    data = {
        'form':form,
        'id':user_id,
        'username':user.admin.email,

    }
    return render(request,'users/edit_user.html',data)

# def Edit_User_Save(request):
#     if request.method != 'POST':
#         return HttpResponse("Method Not Allowed")
#     else:
#         user_id = request.session.get('user_id')
#         if user_id == None:
#             return redirect('manage_user')
        
#         form = EditUserForm(request.POST,request.FILES)
#         if form.is_valid():
#         # profile_pic = request.FILES.get("profile_pic")
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             profile_pic = request.FILES.get('profile_pic')
#             if profile_pic:
#                 fs = FileSystemStorage()
#                 filename = fs.save(profile_pic.name,profile_pic)
#                 profile_pic_url = fs.url(filename)
#             else:
#                 profile_pic_url = None

#             try:
#                 user = CustomUser.objects.get(id = user_id)
#                 user.first_name = first_name
#                 user.last_name = last_name
#                 user.username = username
#                 user.email = email
#                 user.save()

#                 user_model = User.objects.get(admin = user_id)
                
#                 if profile_pic_url != None:
#                     user_model.profile_pic = profile_pic_url
#                 user_model.save()
#                 del request.session['user_id']
#                 messages.success(request,"Successfully Edited User")
#                 return redirect('manage_user')
#             except:
#                 messages.error(request,"Failed to Edit User")
#                 return redirect('manage_user')
#         else:
#             form = EditUserForm(request.POST)
#             user = User.objects.get(admin = user_id)
#             return render(request,"users/edit_user.html",{'form':form,'id':user_id,'username':user.admin.email})
# @method_decorator(utils.super_admin_only, name='dispatch')
# class JobAdd(View):
#     model = common_model.Job
#     form_class = forms.JobForm
#     template = app + "job_add.html"

#     def get(self,request):
#         job_list = self.model.objects.all().order_by('-id')
#         context = {
#             "job_list" : job_list,
#             "form": self.form_class,
#         }
#         return render(request, self.template, context)
    
#     def post(self, request):

#         form = self.form_class(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"job is added successfully.....")
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f'{field}: {error}')

#         return redirect("admin_dashboard:job_list")
