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


@method_decorator(utils.super_admin_only, name='dispatch')
class ApplicationList(View):
    model = common_model.Application
    template = app + "job_list.html"

    def get(self,request):
        application_list = self.model.objects.all().order_by('-id')
        
        paginated_data = utils.paginate(
            request, application_list, 50
        )
        context = {
            "application_list":application_list,
            "data_list":paginated_data
        }
        return render(request, self.template, context)
    


class ApplicationList(View):
    model = common_model.Application
    template = app + "job_list.html"

    def get(self,request):
        application_list = self.model.objects.all().order_by('-id')
        
        paginated_data = utils.paginate(
            request, application_list, 50
        )
        context = {
            "application_list":application_list,
            "data_list":paginated_data
        }
        return render(request, self.template, context)


@method_decorator(utils.super_admin_only, name='dispatch')
class JobSearch(View):
    model = common_model.Job
    form_class = forms.CatagoryEntryForm
    template = app + "job_list.html"

    def post(self,request):
        filter_by = request.POST.get("filter_by")
        query = request.POST.get("query")
        job_list = []
        if filter_by == "uid":
            job_list = self.model.objects.filter(id = query)
        else:
            job_list = self.model.objects.filter(title__icontains = query)

        paginated_data = utils.paginate(
            request, job_list, 50
        )
        context = {
            "form": self.form_class,
            "job_list":job_list,
            "data_list":paginated_data
        }
        return render(request, self.template, context)



class JobSearch(View):
    model = common_model.Job
    form_class = forms.CatagoryEntryForm
    template = app + "job_list.html"

    def post(self,request):
        filter_by = request.POST.get("filter_by")
        query = request.POST.get("query")
        job_list = []
        if filter_by == "uid":
            job_list = self.model.objects.filter(id = query)
        else:
            job_list = self.model.objects.filter(title__icontains = query)

        paginated_data = utils.paginate(
            request, job_list, 50
        )
        context = {
            "form": self.form_class,
            "job_list":job_list,
            "data_list":paginated_data
        }
        return render(request, self.template, context)

@method_decorator(utils.super_admin_only, name='dispatch')
class JobFilter(View):
    model = common_model.Job
    template = app + "job_list.html"

    def get(self,request):
        filter_by = request.GET.get("filter_by")


        if filter_by == "show_as_new":
            job_list = self.model.objects.filter(show_as_new="yes").order_by('-id')


        elif filter_by == "hide":
            job_list = self.model.objects.filter(hide="yes").order_by('-id')        

        else:
            job_list = self.model.objects.filter().order_by('-id')

        paginated_data = utils.paginate(
            request, job_list, 50
        )

        context = {
            "job_list":job_list,
            "data_list":paginated_data
        }
        return render(request, self.template, context)
    

class JobFilter(View):
    model = common_model.Job
    template = app + "job_list.html"

    def get(self,request):
        filter_by = request.GET.get("filter_by")

        if filter_by == "show_as_new":
            job_list = self.model.objects.filter(show_as_new="yes").order_by('-id')

        elif filter_by == "hide":
            job_list = self.model.objects.filter(hide="yes").order_by('-id')        

        else:
            job_list = self.model.objects.filter().order_by('-id')

        paginated_data = utils.paginate(
            request, job_list, 50
        )

        context = {
            "job_list":job_list,
            "data_list":paginated_data
        }
        return render(request, self.template, context)
    

@method_decorator(utils.super_admin_only, name='dispatch')
class APIJobFilter(View):
    model = common_model.Job
    template = app + "job_list.html"

    def get(self,request):
        filter_by = request.GET.get("filter_by", None)

        if filter_by == "show_as_new":
            job_list = self.model.objects.filter(show_as_new="yes").order_by('-id')

        elif filter_by == "hide":
            job_list = self.model.objects.filter(hide="yes").order_by('-id') 

        elif filter_by == "catagory":
            job_list = self.model.objects.filter(catagory="yes").order_by('-id')      

        else:
            job_list = self.model.objects.filter().order_by('-id')

        paginated_data = utils.paginate(
            request, job_list, 50
        )
        
        context = {
            "job_list":job_list,
            "data_list":paginated_data
        }
        return render(request, self.template, context)



class CatagoryJobFilter(APIView):
    permission_classes = [api_permission.is_authenticated]
    serializer_class= job_serializer.jobSerializer
    model= common_model.Job
    pagination_class = utils.CustomPagination(50)


    @swagger_auto_schema(
        tags=["job"],
        operation_description="job List as per catagory...",
    )
    def get(self,request, catagory_id ):
        
        job_list = self.model.objects.filter(category__id = catagory_id).order_by('-id')

        paginator = self.pagination_class
        page = paginator.paginate_queryset(job_list, request)
        serialized_data= self.serializer_class(page, many=True).data

        return Response({
            'status': 200,
            'job_list': serialized_data,
            'pagination_meta_data': paginator.pagination_meta_data(),

        })


class ApiJobList(APIView):

    permission_classes = [api_permission.is_authenticated]
    serializer_class= job_serializer.jobSerializer
    model= common_model.Job
    pagination_class = utils.CustomPagination(50)

    @swagger_auto_schema(
        tags=["job"],
        operation_description="It will return job list. Available filters: ['hide','all']",
        manual_parameters=swagger_doc.job_filter,
    )
    def get(self, request):

        filter_by = request.GET.get("filter_by", None)

        if filter_by == "show_as_new":
            job_list = self.model.objects.filter(show_as_new="yes").order_by('-id')

        elif filter_by == "hide":
            job_list = self.model.objects.filter(hide="yes").order_by('-id')        

        else:
            job_list = self.model.objects.filter().order_by('-id')

        paginator = self.pagination_class
        page = paginator.paginate_queryset(job_list, request)
        serialized_data= self.serializer_class(page, many=True).data

        return Response({
            'status': 200,
            'job_list': serialized_data,
            'pagination_meta_data': paginator.pagination_meta_data(),

        })


class ApiJobDetail(APIView):

    permission_classes = [api_permission.is_authenticated]
    serializer_class= job_serializer.jobSerializer
    model= common_model.Job

    @swagger_auto_schema(
        tags=["job"],
        operation_description="job Detail API",
    )
    def get(self, request, job_uid):

        job = self.model.objects.get(id = job_uid)
        serialized_data= self.serializer_class(job).data

        return Response({
            'status': 200,
            'job': serialized_data,

        })

@method_decorator(utils.super_admin_only, name='dispatch')
class JobAdd(View):
    model = common_model.Job
    form_class = forms.JobForm
    template = app + "job_add.html"

    def get(self,request):
        job_list = self.model.objects.all().order_by('-id')
        context = {
            "job_list" : job_list,
            "form": self.form_class,
        }
        return render(request, self.template, context)
    
    def post(self, request):

        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"job is added successfully.....")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return redirect("admin_dashboard:job_list")


@method_decorator(utils.super_admin_only, name='dispatch')
class JobUpdate(View):
    model = common_model.Job
    form_class = forms.JobForm
    template = app + "job_update.html"

    def get(self,request, job_uid):
        job = self.model.objects.get(id = job_uid)
 
        context = {
            "job" : job,
            "form": self.form_class(instance=job),
        }
        return render(request, self.template, context)
    
    def post(self,request, job_uid):

        job = self.model.objects.get(id = job_uid)
        form = self.form_class(request.POST, request.FILES, instance=job)

        if form.is_valid():
            form.save()
            messages.success(request, f"job ({job_uid}) is updated successfully.....")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return redirect("admin_dashboard:job_update", job_uid = job_uid)


@method_decorator(utils.super_admin_only, name='dispatch')
class JobDelete(View):
    model = common_model.Job

    def get(self,request, job_uid):
        job = self.model.objects.get(id = job_uid)

        if job.image:
            image_path = job.image.path
            os.remove(image_path)

        job.delete()
        messages.info(request, 'job is deleted succesfully......')

        return redirect("admin_dashboard:job_list")