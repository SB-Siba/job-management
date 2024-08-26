from django.shortcuts import render, redirect , HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from helpers import utils, api_permission
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from user import forms as siteforms
from admin_dashboard.manage_product import forms
import os
from app_common import models as common_model
from user import forms
from .forms import EditUserForm,AddUserForm,JobSelectionForm,CategoryFilterForm
import logging
from django.http import JsonResponse
from django.urls import reverse_lazy
from .forms import EmployeeForm 


logger = logging.getLogger(__name__)
app = "admin_dashboard/users/"


class UserList(View):
    model = common_model.User
    template = app + "user_list.html"

    def get(self, request):
        category_form = CategoryFilterForm()
        user_obj = self.model.objects.filter(is_superuser=False, is_staff=False).order_by("id")
        return render(request, self.template, {"user_obj": user_obj, "category_form": category_form})

    def post(self, request):
        category_form = CategoryFilterForm(request.POST)
        job_form = None
        category = None

        if category_form.is_valid():
            category = category_form.cleaned_data['category']
            user_obj = common_model.User.objects.filter(category=category, is_superuser=False, is_staff=False)
            job_form = JobSelectionForm(category=category)
            return render(request, self.template, {
                'category_form': category_form,
                'user_obj': user_obj,
                'job_form': job_form,
                'category': category
            })

        if 'category_id' in request.POST:
            category_id = request.POST.get('category_id')
            category = common_model.category.objects.get(id=category_id)
            job_form = JobSelectionForm(request.POST, category=category)
            user_obj = common_model.User.objects.filter(category=category, is_superuser=False, is_staff=False)

            if job_form.is_valid():
                selected_jobs = job_form.cleaned_data['jobs']
                job_list = "\n".join([f"{job.title} - {job.company_name}" for job in selected_jobs])

                action = request.POST.get('action')
                if action == 'send_selected':
                    selected_user_ids = request.POST.getlist('selected_users')
                    users_to_send = user_obj.filter(id__in=selected_user_ids)
                else:  # send_all
                    users_to_send = user_obj

                admin_email = "noreplyf577@gmail.com"

                success_messages = []
                error_messages = []

                for user in users_to_send:
                    try:
                        send_mail(
                            'Job Opportunities',
                            f'Dear {user.full_name},\n\nHere are some job opportunities you might be interested in:\n\n{job_list}',
                            admin_email,
                            [user.email],
                            fail_silently=False,
                        )
                        success_messages.append(f"Email sent to {user.full_name} ({user.email})")
                    except Exception as e:
                        error_messages.append(f"Failed to send email to {user.full_name} ({user.email}): {e}")

                for msg in success_messages:
                    messages.success(request, msg)
                for msg in error_messages:
                    messages.error(request, msg)

                return redirect('admin_dashboard:userslist')

        user_obj = self.model.objects.filter(is_superuser=False, is_staff=False).order_by("id")
        return render(request, self.template, {"user_obj": user_obj, "category_form": category_form, "job_form": job_form})



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
        # messages.error(request, "User with this Email already exists")
        return render(request, self.template, {'form': form})


class DeleteUser(View):
    template = app+ "user_list.html"

    def post(self, request, user_id):
        user = get_object_or_404(common_model.User, id=user_id)
        user.delete()
        messages.success(request, f'User {user.full_name} deleted successfully.')
        return redirect('admin_dashboard:user_list')

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


class EmployeeList(View):
    model = common_model.User
    template = app + "employee_list.html"

    def get(self, request):
        employees = self.model.objects.filter(is_employee=True).order_by("id")
        return render(request, self.template, {"employees": employees})

class AdminEmployeeAssignView(View):
    template_name = 'admin_employee_assign.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        jobs = Job.objects.filter(application__user=user)  # Get jobs where the user has applied
        context = {
            'user': user,
            'jobs': jobs,
        }
        return render(request, self.template_name, context)

    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, pk=job_id)

        # Mark user as an employee
        user.is_employee = True
        user.save()

        # Optionally, you can perform additional actions like notifying the user or updating job-related information
        
        messages.success(request, f'{user.full_name} has been assigned as an employee.')

        return redirect('admin_dashboard:employee_list')


@method_decorator(utils.super_admin_only, name='dispatch')
class EmployeeList(View):
    template_name = app + 'employee_list.html'
    
    def get(self, request):
        employees = common_model.Employee.objects.all()
        context = {
            'employees': employees
        }
        return render(request, self.template_name, context)
@method_decorator(utils.super_admin_only, name='dispatch')
class EmployeeDetail(View):
    model = common_model.Employee
    template_name = app + "employee_detail.html"

    def get(self, request, employee_id):
        employee = get_object_or_404(self.model, id=employee_id)
        context = {
            "employee": employee,
        }
        return render(request, self.template_name, context)
    
class EmployeeEditView(View):
    template_name = 'admin_dashboard/users/employee_update.html'
    form_class = EmployeeForm


    def get(self, request, employee_id):
        # Fetch the employee object based on the ID
        employee = get_object_or_404(common_model.Employee, id=employee_id)
        print (employee, "==================")
        # Create a form instance and populate it with data from the employee instance
        form = self.form_class(instance=employee)
        
        # Add user-related initial values for the form fields
        form.fields['user_full_name'].initial = employee.user.full_name
        form.fields['user_email'].initial = employee.user.email
        form.fields['contact'].initial = employee.user.contact

        # Context data to render the template
        context = {
            'form': form,
            'employee_id': employee_id,
            'employee_name': employee.user.full_name,
        }
        return render(request, self.template_name, context)

    def post(self, request, employee_id):
        # Fetch the employee object based on the ID
        employee = get_object_or_404(common_model.Employee, pk=employee_id)
        # Bind form data to the form instance
        form = self.form_class(request.POST, instance=employee)

        if form.is_valid():
            # Update the user-related fields
            employee.user.full_name = form.cleaned_data['user_full_name']
            employee.user.email = form.cleaned_data['user_email']
            employee.user.contact = form.cleaned_data['contact']
            # Save the user and employee
            employee.user.save()
            form.save()
            return redirect('admin_dashboard:employee_list')
        
        else:
            messages(request, "invild Details")
            return redirect('admin_dashboard:employee_list')
    

class DeleteEmployee(View):
    def post(self, request, employee_id):
        # Fetch the employee object based on the ID
        employee = get_object_or_404(common_model.Employee, id=employee_id)
        # Delete the employee
        employee.delete()
        # Set a success message
        messages.success(request, f'Employee {employee.user.full_name} deleted successfully.')
        # Redirect to the employee list view
        return redirect('admin_dashboard:employee_list')