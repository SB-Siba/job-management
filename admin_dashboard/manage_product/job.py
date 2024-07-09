from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.conf import settings
#import requests
from django.http import JsonResponse
import json
from helpers import utils, api_permission
from django.forms.models import model_to_dict
import os
from django.shortcuts import get_object_or_404
from django.utils import timezone
# for api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
# -------------------------------------------- custom import
from .. import swagger_doc
from . import serializer as job_serializer
from . import forms
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
    template_name = app +'edit_job.html'
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
        
@method_decorator(utils.super_admin_only, name='dispatch')
class ApplicationList(View):
    model = common_model.Application
    template = app + "application_list.html"

    def get(self, request):
        application_list = self.model.objects.all().order_by('-id')
        paginated_data = utils.paginate(request, application_list, 50)
        context = {
            "application_list": application_list,
            "data_list": paginated_data
        }
        return render(request, self.template, context)

    def post(self, request):
        application_list = self.model.objects.all().order_by('-id')
        for application in application_list:
            new_status = request.POST.get(f'status_{application.id}')
            if new_status:
                application.status = new_status
                application.save()
        messages.success(request, 'The statuses of the selected candidates have been updated.')
        return redirect('admin_dashboard:application_list')
@method_decorator(utils.super_admin_only, name='dispatch')
class JobSearch(View):
    model =common_model.Job
    form_class = forms.CatagoryEntryForm
    template = app + "job_list.html"

    def post(self, request):
        filter_by = request.POST.get("filter_by")   
        query = request.POST.get("query")
        if filter_by == "uid":
            job_list = self.model.objects.filter(id=query)
        else:
             job_list = self.model.objects.filter(catagory__title__icontains=query)

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
        if filter_by == "catagory":
            catagory_id = request.GET.get("catagory_id")
            job_list = self.model.objects.filter(catagory_id=catagory_id).order_by('-id')
        else:
            job_list = self.model.objects.all().order_by('-id')

        paginated_data = utils.paginate(request, job_list, 50)
        context = {
            "job_list": job_list,
            "data_list": paginated_data
        }
        return render(request, self.template, context)

class JobDetail(View):
    model =common_model.Job
    template = app +"job_detail.html"

    def get(self, request, job_uid):
        job = get_object_or_404(self.model, id=job_uid)
        applications_count = common_model.Application.objects.filter(job=job).count()
        employees = common_model.Application.objects.filter(job=job,status='Hired')
        client = job.client
        context = {
            "job": job,
            'applications_count': applications_count,
            "employees": employees,
            "client": client,
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
                job.client = form.cleaned_data['client']
            job.status = 'unpublished'
            job.save()
            messages.success(request, 'Job added successfully.')
            return redirect('admin_dashboard:job_list')
        return render(request, self.template, {'form': form})



@method_decorator(utils.super_admin_only, name='dispatch')
class JobDelete(View):
    model = common_model.Job

    def get(self, request, job_uid):
        job = get_object_or_404(self.model, id=job_uid)
        job.delete()
        messages.info(request, 'Job deleted successfully.')

        return redirect("admin_dashboard:job_list")



        