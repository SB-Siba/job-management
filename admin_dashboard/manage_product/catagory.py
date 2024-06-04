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


app = "admin_dashboard/manage_product/"

# ================================================== patient management ==========================================

@method_decorator(utils.super_admin_only, name='dispatch')
class CatagotyList(View):
    model = common_model.Category
    form_class = forms.CategoryEntryForm
    template = app + "catagory_list.html"

    def get(self,request):
        catagory_list = self.model.objects.all().order_by('-id')
        categories = []
        product_count = []
        for i in catagory_list:
            p_obj = common_model.AudioBook.objects.filter(category = i).count()
            categories.append(i)
            product_count.append(p_obj)

        category_product_count_zip = zip(categories,product_count)
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

        return redirect("admin_dashboard:catagory_list")


@method_decorator(utils.super_admin_only, name='dispatch')
class CatagotyUpdate(View):
    model = common_model.Category
    form_class = forms.CategoryEntryForm
    template = app + "catagory_update.html"

    def get(self,request, catagory_id):
        catagory = self.model.objects.get(id= catagory_id)
        context = {
            "form": self.form_class(instance=catagory),
        }
        return render(request, self.template, context)
    
    def post(self, request, catagory_id):
        catagory = self.model.objects.get(id= catagory_id)
        form = self.form_class(request.POST, request.FILES ,instance= catagory)
        if form.is_valid():
            form.save()
            messages.success(request, f"{request.POST['title']} is updated successfully.....")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return redirect("admin_dashboard:catagory_update", catagory_id = catagory_id)


@method_decorator(utils.super_admin_only, name='dispatch')
class CatagotyDelete(View):
    model = common_model.Category
    form_class = forms.CategoryEntryForm
    template = app + "catagory_update.html"

    def get(self,request, catagory_id):
        catagory = self.model.objects.get(id= catagory_id).delete()
        messages.info(request, "Catagory is deleted successfully....")
        return redirect("admin_dashboard:catagory_list")


class CatagotyListApi(APIView):

    permission_classes = [api_permission.is_authenticated]
    serializer_class= product_serializer.CatagorySerializer
    model= common_model.Category
    pagination_class = utils.CustomPagination(50)

    @swagger_auto_schema(
        tags=["catagory"],
        operation_description="It will return all catagory list",
    )

    def get(self, request):

        catagory_list= self.model.objects.filter(hide="no").order_by('-id')
        print(catagory_list)
        paginator = self.pagination_class
        page = paginator.paginate_queryset(catagory_list, request)
        serialized_data= self.serializer_class(page, many=True).data

        return Response({
            'status': 200,
            'catagory_list': serialized_data,
            'pagination_meta_data': paginator.pagination_meta_data(),

        })
