from django.shortcuts import render, redirect , HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from helpers import utils, api_permission
from django.contrib import messages
from user import forms as siteforms
from admin_dashboard.manage_product import forms
import os
from app_common import models as common_model
from user import forms
from .forms import EditUserForm,AddUserForm
app = "admin_dashboard/users/"

# def candidate_list(request):
#     candidates = Candidate.objects.all()
#     return render(request, 'user_list.html', {'candidates': candidates})

# def candidate_detail(request, candidate_id):
#     candidate = Candidate.objects.get(id=candidate_id)
#     return render(request, 'user_detail.html', {'candidate': candidate})

# def assign_category(request, candidate_id):
#     candidate = Candidate.objects.get(id=candidate_id)
#     if request.method == 'POST':
#         category = request.POST.get('category')
#         candidate.category = catagory
#         candidate.save()
#         return redirect('candidate_detail', candidate_id=candidate.id)
#     return render(request, 'candidates/assign_category.html', {'candidate': candidate})

# def update_status_hired(request, candidate_id):
#     candidate = Candidate.objects.get(id=candidate_id)
#     candidate.status = 'hired'
#     candidate.save()
#     return redirect('candidate_detail', candidate_id=candidate.id)


class UserList(View):
    model = common_model.User
    template = app + "user_list.html"

    def get(self,request):
        user_obj = self.model.objects.filter(is_superuser=False).order_by("id")
        return render(request,self.template,{"user_obj":user_obj})
    
class AddUserView(View):
    template = app + "user_add.html"
    form_class = AddUserForm
    def get(self, request):
        form = self.form_class()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Ensure the password is hashed
            user.save()
            messages.success(request, f"User {user.full_name} has been successfully added.")
            return redirect('admin_dashboard:userslist')
        messages.error(request, "There was an error adding the user. Please check the details and try again.")
        return render(request, self.template, {'form': form})


class DeleteUser(View):
    model = common_model.User
    template = app + "confirm_delete.html"  # A template to confirm deletion

    def get(self, request, user_id):
        user = get_object_or_404(self.model, id=user_id)
        return render(request, self.template, {"user": user})

    def post(self, request, user_id):
        user = get_object_or_404(self.model, id=user_id)
        user.delete()
        messages.success(request, f"User {user.full_name} has been successfully deleted.")
        return redirect('admin_dashboard:userslist')


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



