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
from .forms import EditUserForm
app = "admin_dashboard/users/"

def candidate_list(request):
    candidates = Candidate.objects.all()
    return render(request, 'user_list.html', {'candidates': candidates})

def candidate_detail(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)
    return render(request, 'user_detail.html', {'candidate': candidate})

def assign_category(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)
    if request.method == 'POST':
        category = request.POST.get('category')
        candidate.category = catagory
        candidate.save()
        return redirect('candidate_detail', candidate_id=candidate.id)
    return render(request, 'candidates/assign_category.html', {'candidate': candidate})

def update_status_hired(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)
    candidate.status = 'hired'
    candidate.save()
    return redirect('candidate_detail', candidate_id=candidate.id)


class UserList(View):
    model = common_model.User
    template = app + "user_list.html"

    def get(self,request):
        user_obj = self.model.objects.filter(is_superuser=False).order_by("id")
        return render(request,self.template,{"user_obj":user_obj})
    

class DeleteUser(View):  
    def get(self,request,user_id):
        print("hiii")
        user = common_model.User.objects.get(id=user_id)
        print(user)
        if user:
            user.delete()
        return redirect('admin_dashboard:admin_dashboard')

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

class UserDetailView(View):
    model = common_model.User
    template = app + "user_profile.html"
    def get(self,request,user_id):
        user_obj = self.model.objects.get(id=user_id)
        return render(request, self.template, {"user_obj": user_obj})

class Edit_User(View):
    template = app + "edit_user.html"
    def get(self,request,user_id):
        user = common_model.User.objects.get(pk = user_id)
        form = EditUserForm()
        form.fields['email'].initial = user.email
        form.fields['full_name'].initial = user.full_name
        form.fields['contact'].initial = user.contact


        data = {
            'form':form,
            'id':user_id,
            'username':user.email,

        }
        return render(request,self.template,data)
    def post(self,request,user_id):
        user = common_model.User.objects.get(pk = user_id)

        form = EditUserForm(request.POST)
        if form.is_valid:
            email = request.POST.get("email")
            full_name = request.POST.get("full_name")
            contact = request.POST.get("contact")

            user.email = email
            user.full_name = full_name
            user.contact = contact
            user.save()

        return redirect("admin_dashboard:user_detail",user_id)



