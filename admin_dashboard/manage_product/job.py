from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.conf import settings
#import requests
from django.db import transaction
from django.http import FileResponse, Http404, JsonResponse,HttpResponse
import json

from requests import request
from helpers import utils, api_permission
from django.forms.models import model_to_dict
import os
from django.shortcuts import get_object_or_404
from django.utils import timezone
# for api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
# -------------------------------------------- custom import
from .. import swagger_doc
from . import serializer as job_serializer
from . import forms
from django.core.exceptions import MultipleObjectsReturned
from app_common import models as common_model

app = "admin_dashboard/manage_product/"

# ================================================== product management ==========================================

@method_decorator(utils.super_admin_only, name='dispatch')
class JobList(View):
    model = common_model.Job
    template = app + "job_list.html"

    def get(self,request):
        job_list = self.model.objects.all().order_by('-id')
        
        paginated_data = utils.paginate(
            request, job_list, 50
        )
        context = {
            "job_list":job_list,
            "data_list":paginated_data
        }
        return render(request, self.template, context)
    def post(self, request):
        job_id = request.POST.get("job_id")
        job = get_object_or_404(common_model.Job, id=job_id)

        return redirect("admin_dashboard:job_list")


@method_decorator(utils.super_admin_only, name='dispatch')
class JobEdit(View):
    template_name = app + 'edit_job.html'
    model = common_model.Job
    form_class = forms.JobForm

    def get(self, request, job_id):
        job = get_object_or_404(self.model, id=job_id)
        form = forms.JobForm(instance=job, user=request.user)
        return render(request, self.template_name, {'form': form, 'job': job})

    def post(self, request, job_id):
        job = get_object_or_404(self.model, id=job_id)
        form = forms.JobForm(request.POST, request.FILES, instance=job, user=request.user)
        if form.is_valid():
            job = form.save(commit=False)
            if job.status == 'published':
                job.published_date = timezone.now()
            else:
                job.published_date = None
            job.save()
            messages.success(request, f'Job "{job.title}" updated successfully.')
            return redirect('admin_dashboard:job_list')
        return render(request, self.template_name, {'form': form, 'job': job})
        

class DeleteAllDataView(View):
    def get(self, request):
        try:
            common_model.Job.objects.all().delete()
            common_model.Application.objects.all().delete()
          

 
            message = "All data deleted successfully."
            status_code = 200
        except Exception as e:
            message = f"Failed to delete data: {str(e)}"
            status_code = 500
        return HttpResponse(message, status=status_code)



    template = app + "application_list.html"

    def get(self, request):
        applications = common_model.Application.objects.all()

        application_status_options = []
        for application in applications:
            status_options = {
                'id': application.id,
                'user_full_name': application.user.full_name,
                'job_category': application.job.category if application.job else 'No category available',
                'company_name': application.job.company_name if application.job else 'No company available',
                'email': application.email,
                'contact': application.contact,
                'applied_at': application.applied_at,
                'status_options': [
                    {'value': 'Applied', 'selected': application.status == 'Applied'},
                    {'value': 'Interviewed', 'selected': application.status == 'Interviewed'},
                    {'value': 'Hired', 'selected': application.status == 'Hired'},
                    {'value': 'Rejected', 'selected': application.status == 'Rejected'},
                ],
            }
            application_status_options.append(status_options)

        context = {
            "applications": applications,
            "application_status_options": application_status_options,
            
        }
        return render(request, self.template, context)

    # def post(self, request):
    #     updated = False
    
    #     application_number = request.POST.get("application_number")
    #     status = request.POST.get("status")
    
    #     print(application_number, status, "lklklk")
    
    #     application = None  # Initialize the application variable
    
    #     try:
    #         application = common_model.Application.objects.get(id=application_number)
    #         print(application, "Applic")
    #     except common_model.Application.DoesNotExist:
    #         messages.error(request, f"Application with ID {application_number} does not exist.")
    #         return redirect('admin_dashboard:application_list')  # Exit early if application doesn't exist
    
    #     # Proceed only if the application is found
    #     if application.status != status:
    #         application.status = status
    #         application.save()
    #         updated = True
    
    #         if status == 'Hired':
    #             try:
    #                 existing_employees = common_model.Employee.objects.filter(
    #                     user=application.user,
    #                     job=application.job,
    #                     employer=application.job.client
    #                 )
    #                 if existing_employees.exists():
    #                     messages.warning(
    #                         request,
    #                         f"{application.email} is already hired for the {application.job.category} role."
    #                     )
    #                 else:
    #                     common_model.Employee.objects.create(
    #                         user=application.user,
    #                         employer=application.job.client,
    #                         job=application.job,
    #                         application=application,
    #                         salary=0,
    #                         period_start=timezone.now(),
    #                         period_end=timezone.now() + timezone.timedelta(days=365),
    #                     )
    #                     messages.success(
    #                         request, f'{application.user.full_name} has been hired successfully for the {application.job.category} role.'
    #                     )
    #             except MultipleObjectsReturned:
    #                 messages.error(
    #                     request,
    #                     f"Multiple entries found for {application.email}. Please check for duplicate records."
    #                 )
    
    #     if updated:
    #         messages.success(request, 'Application status updated successfully.')
    #     else:
    #         messages.info(request, 'No changes were made to the application statuses.')
    
    #     return redirect('admin_dashboard:application_list')
@method_decorator(utils.super_admin_only, name='dispatch')
class ApplicationList(View):
    template = app + "application_list.html"

    def get(self, request):
        applications = common_model.Application.objects.all()
        application_status_options = []

        for application in applications:
            status_options = {
                'id': application.id,
                'user_full_name': application.user.full_name,
                'job_category': application.job.category if application.job else 'No category available',
                'company_name': application.job.company_name if application.job else 'No company available',
                'email': application.email,
                'contact': application.contact,
                'applied_at': application.applied_at,
                'status_options': [
                    {'value': 'Applied', 'selected': application.status == 'Applied'},
                    {'value': 'Interviewed', 'selected': application.status == 'Interviewed'},
                    {'value': 'Hired', 'selected': application.status == 'Hired'},
                    {'value': 'Rejected', 'selected': application.status == 'Rejected'},
                ],
            }
            application_status_options.append(status_options)

        context = {
            "applications": applications,
            "application_status_options": application_status_options,
        }
        return render(request, self.template, context)

    def post(self, request):
        application_id = request.POST.get('application_id')
        new_status = request.POST.get('status')

        try:
            application = common_model.Application.objects.get(id=application_id)
            previous_status = application.status  # Store previous status for checking
            
            # Update application status
            application.status = new_status
            application.save()

            # If status is changed to 'Hired', check if the Employee record already exists
            if new_status == 'Hired' and previous_status != 'Hired':
                employee, created = common_model.Employee.objects.get_or_create(
                    user=application.user,
                    job=application.job,
                    sector = application.job.sector,
                    application = application,
                    defaults={'salary': 0.00}  # You can set other defaults here as well
                )

                if not created:
                    # Handle the case where the Employee record already exists
                    # You could log this or notify the user, depending on your needs
                    print(f"Employee record already exists for user {application.user.id} and job {application.job.id}")

            return redirect('admin_dashboard:application_list')  # Redirect to the application list page
        except common_model.Application.DoesNotExist:
            # Handle case where application doesn't exist
            return render(request, self.template, {'error': 'Application not found'})


@method_decorator(utils.super_admin_only, name='dispatch')
class JobSearch(View):
    model =common_model.Job
    form_class = forms.categoryEntryForm
    template = app + "job_list.html"

    def post(self, request):
        filter_by = request.POST.get("filter_by")   
        query = request.POST.get("query")
        if filter_by == "uid":
            job_list = self.model.objects.filter(id=query)
        else:
             job_list = self.model.objects.filter(category__title__icontains=query)

        paginated_data = utils.paginate(request, job_list, 50)
        context = {
            "form": self.form_class,
            "job_list": job_list,
            "data_list": paginated_data
        }
        return render(request, self.template, context)

@method_decorator(utils.super_admin_only, name='dispatch')
class JobFilter(View):
    model = common_model.Job
    template =  app + "job_list.html"

    def get(self, request):
        filter_by = request.GET.get("filter_by")
        if filter_by == "category":
            category_id = request.GET.get("category_id")
            job_list = self.model.objects.filter(category_id=category_id).order_by('-id')
        else:
            job_list = self.model.objects.all().order_by('-id')

        paginated_data = utils.paginate(request, job_list, 50)
        context = {
            "job_list": job_list,
            "data_list": paginated_data
        }
        return render(request, self.template, context)


@method_decorator(utils.super_admin_only, name='dispatch')
class JobDetail(View):
    model =common_model.Job
    template = app +"job_detail.html"

    def get(self, request, job_uid):
        job = get_object_or_404(self.model, id=job_uid)
        applications_count = common_model.Application.objects.filter(job=job).count()
        employees = common_model.Application.objects.filter(job=job,status='Hired')
        applications = common_model.Application.objects.filter(job=job)
        sector = job.sector
        context = {
            "job": job,
            'applications_count': applications_count,
            "employees": employees,
            "sector": sector,
            "applications": applications,

        }
        return render(request, self.template, context)
   
     

@method_decorator(utils.super_admin_only, name='dispatch')
class JobAdd(View):
    model = common_model.Job
    template = app + "job_add.html"

    def get(self, request):
        form = forms.JobForm(user=request.user)
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = forms.JobForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            job = form.save(commit=False)
            if request.user.is_superuser:
                job.sector = form.cleaned_data['sector']
            if form.cleaned_data['status'] == 'published':
                job.status = 'published'
            else:
                job.status = 'unpublished'
            job.save()
            messages.success(request, 'Job added successfully.')
            return redirect('admin_dashboard:job_list')
        return render(request, self.template, {'form': form})

@method_decorator(utils.super_admin_only, name='dispatch')
class JobDelete(View):
    model = common_model.Job

    def post(self, request, job_uid):
        job = get_object_or_404(self.model, id=job_uid)
        job.delete()
        messages.info(request, 'Job deleted successfully.')
        return redirect('admin_dashboard:job_list')

def download_resume(request, application_id):
    application = get_object_or_404(common_model.Application, id=application_id)
    
    if application.user_resume:
        file_path = os.path.join(settings.MEDIA_ROOT, application.user_resume.name)
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True)
        else:
            raise Http404("Resume not found")
    else:
        raise Http404("No resume uploaded")