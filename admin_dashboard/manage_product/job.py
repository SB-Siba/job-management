from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from helpers import utils, api_permission
from django.contrib import messages
from . import forms
import os
from app_common import models as common_model


app = "admin_dashboard/job/"


@method_decorator(utils.super_admin_only, name='dispatch')
class JobList(View):
    model = common_model.job
    template = app + "job_list.html"

    def get(self,request):
        job_list = self.model.objects.all().order_by('id')
        
        paginated_data = utils.paginate(
            request, job_list, 50
        )
        context = {
            "job_list":job_list,
            "data_list":paginated_data
        }
        return render(request, self.template, context)
    
class JobList(View):
    model = common_model.job
    template = app + "job_list.html"

    def get(self,request):
        job_list = self.model.objects.all().order_by('id')
        
        paginated_data = utils.paginate(
            request, job_list, 50
        )
        context = {
            "job_list":job_list,
            "data_list":paginated_data
        }
        return render(request, self.template, context)
    
@method_decorator(utils.super_admin_only, name='dispatch')
class JobSearch(View):
    model = common_model.job
    form_class = forms.CategoryEntryForm
    template = app + "job_list.html"

    def post(self,request):
        filter_by = request.POST.get("filter_by")
        query = request.POST.get("query")
        product_list = []
        if filter_by == "uid":
            job_list = self.model.objects.filter(e_id = query)
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
    model = common_model.job
    form_class = forms.CategoryEntryForm
    template = app + "job_list.html"

    def post(self,request):
        filter_by = request.POST.get("filter_by")
        query = request.POST.get("query")
        product_list = []
        if filter_by == "uid":
            job_list = self.model.objects.filter(e_id = query)
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
class JobAdd(View):
    model = common_model.job
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
            messages.success(request, f"Job is added successfully.....")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return redirect("admin_dashboard:job_list")
    
@method_decorator(utils.super_admin_only, name='dispatch')
class JobUpdate(View):
    model = common_model.job
    form_class = forms.JobForm
    template = app + "job_update.html"

    def get(self,request, job_id):
        job = self.model.objects.get(id = job_id)
 
        context = {
            "job" : job,
            "form": self.form_class(instance=job),
        }
        return render(request, self.template, context)
    
    def post(self,request, job_id):

        job = self.model.objects.get(id = job_id)
        form = self.form_class(request.POST, request.FILES, instance=job)

        if form.is_valid():
            form.save()
            messages.success(request, f"Job ({job_id}) is updated successfully.....")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return redirect("admin_dashboard:job_update", job_id = job_id)


@method_decorator(utils.super_admin_only, name='dispatch')
class JobDelete(View):
    model = common_model.job

    def get(self,request, job_id):
        print(job_id,type(job_id))
        product = self.model.objects.get(id = job_id)

        product.delete()
        messages.info(request, 'Job is deleted succesfully......')

        return redirect("admin_dashboard:job_list")