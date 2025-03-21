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

# for api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
# -------------------------------------------- custom import
from .. import swagger_doc
from . import serializer as product_serializer
from . import forms
from app_common import models as common_model
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


app = "admin_dashboard/manage_product/"

# ================================================== patient management ==========================================

@method_decorator(utils.super_admin_only, name='dispatch')
class categoryList(View):
    model = common_model.Category
    form_class = forms.categoryEntryForm
    template = app + "catagory_list.html"

    def get(self,request):
        
        category_list = self.model.objects.all().order_by('-id')
        categorys = []
        product_count = []
        for i in category_list:
            p_obj = common_model.Job.objects.filter(category = i).count()
            categorys.append(i)
            product_count.append(p_obj)
            
        category_product_count_zip = zip(categorys,product_count)
        context = {
            "form": self.form_class,
            "category_product_count_zip":category_product_count_zip,
        }
        return render(request, self.template, context)
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"{request.POST['title']} is added to list.....")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return redirect("admin_dashboard:category_list")


@method_decorator(utils.super_admin_only, name='dispatch')
class categoryAdd(View):
    model = common_model.Category
    form_class = forms.categoryEntryForm
    template = app + "catagory_add.html"

    def get(self, request):
        category_list = self.model.objects.all().order_by('-id')
        context = {
            "category_list": category_list,
            "form": self.form_class,
        }
        return render(request, self.template, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return redirect("admin_dashboard:category_list")
    
@method_decorator(utils.super_admin_only, name='dispatch')
class categoryUpdate(View):
    model = common_model.Category
    form_class = forms.categoryEntryForm
    template = app + "catagory_update.html"

    def get(self, request, category_id):
        category = self.model.objects.get(id=category_id)
        context = {
            "form": self.form_class(instance=category),
        }
        return render(request, self.template, context)
    
    def post(self, request, category_id):
        category = self.model.objects.get(id=category_id)
        form = self.form_class(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"{request.POST['title']} is updated successfully.")
            # Redirect to the category list view after successful update
            return redirect("admin_dashboard:category_list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            # If form is invalid, stay on the same page to correct errors
            return render(request, self.template, {'form': form})


class CategoryDeleteView(View):
    model = common_model.Category
    success_url = reverse_lazy('admin_dashboard:category_list')

    def post(self, request, *args, **kwargs):
        category_id = kwargs.get('pk')
        category = get_object_or_404(self.model, id=category_id)
        category.delete()
        messages.info(request, 'Category deleted successfully.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return JsonResponse({'success': False}, status=400)


@method_decorator(utils.super_admin_only, name='dispatch')
class SectorList(View):
    model = common_model.Category
    form_class = forms.categoryEntryForm
    template = app + "catagory_list.html"

    def get(self,request):
        
        category_list = self.model.objects.all().order_by('-id')
        categorys = []
        product_count = []
        for i in category_list:
            p_obj = common_model.Job.objects.filter(category = i).count()
            categorys.append(i)
            product_count.append(p_obj)
            
        category_product_count_zip = zip(categorys,product_count)
        context = {
            "form": self.form_class,
            "category_product_count_zip":category_product_count_zip,
        }
        return render(request, self.template, context)
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"{request.POST['title']} is added to list.....")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return redirect("admin_dashboard:category_list")


@method_decorator(utils.super_admin_only, name='dispatch')
class SectorAdd(View):
    model = common_model.Category
    form_class = forms.categoryEntryForm
    template = app + "catagory_add.html"

    def get(self, request):
        category_list = self.model.objects.all().order_by('-id')
        context = {
            "category_list": category_list,
            "form": self.form_class,
        }
        return render(request, self.template, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return redirect("admin_dashboard:category_list")
    
@method_decorator(utils.super_admin_only, name='dispatch')
class SectorUpdate(View):
    model = common_model.Category
    form_class = forms.categoryEntryForm
    template = app + "catagory_update.html"

    def get(self, request, category_id):
        category = self.model.objects.get(id=category_id)
        context = {
            "form": self.form_class(instance=category),
        }
        return render(request, self.template, context)
    
    def post(self, request, category_id):
        category = self.model.objects.get(id=category_id)
        form = self.form_class(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"{request.POST['title']} is updated successfully.")
            # Redirect to the category list view after successful update
            return redirect("admin_dashboard:category_list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            # If form is invalid, stay on the same page to correct errors
            return render(request, self.template, {'form': form})


class SectorDeleteView(View):
    model = common_model.Category
    success_url = reverse_lazy('admin_dashboard:category_list')

    def post(self, request, *args, **kwargs):
        category_id = kwargs.get('pk')
        category = get_object_or_404(self.model, id=category_id)
        category.delete()
        messages.info(request, 'Category deleted successfully.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return JsonResponse({'success': False}, status=400)
