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
class CriteriaList(View):
    model = common_model.Criteria
    form_class = forms.CriteriaEntryForm
    template = app + "criteria_list.html"

    def get(self,request):
        criteria_list = self.model.objects.all().order_by('-id')
        criterias = []
        product_count = []
        for i in criteria_list:
            p_obj = common_model.AudioBook.objects.filter(criteria = i).count()
            criterias.append(i)
            product_count.append(p_obj)

        criteria_product_count_zip = zip(criterias,product_count)
        context = {
            "form": self.form_class,
            "criteria_product_count_zip":criteria_product_count_zip,
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

        return redirect("admin_dashboard:criteria_list")


@method_decorator(utils.super_admin_only, name='dispatch')
class CriteriaUpdate(View):
    model = common_model.Criteria
    form_class = forms.CriteriaEntryForm
    template = app + "criteria_update.html"

    def get(self,request, criteria_id):
        criteria = self.model.objects.get(id= criteria_id)
        context = {
            "form": self.form_class(instance=criteria),
        }
        return render(request, self.template, context)
    
    def post(self, request, criteria_id):
        catagory = self.model.objects.get(id= criteria_id)
        form = self.form_class(request.POST, request.FILES ,instance= catagory)
        if form.is_valid():
            form.save()
            messages.success(request, f"{request.POST['title']} is updated successfully.....")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return redirect("admin_dashboard:criteria_update", catagory_id = criteria_id)


@method_decorator(utils.super_admin_only, name='dispatch')
class CriteriaDelete(View):
    model = common_model.Criteria
    form_class = forms.CriteriaEntryForm
    template = app + "criteria_update.html"

    def get(self,request, criteria_id):
        criteria = self.model.objects.get(id= criteria_id).delete()
        messages.info(request, "Criteria is deleted successfully....")
        return redirect("admin_dashboard:criteria_list")


class CriteriaListApi(APIView):

    permission_classes = [api_permission.is_authenticated]
    serializer_class= product_serializer.CriteriaSerializer
    model= common_model.Criteria
    pagination_class = utils.CustomPagination(50)

    @swagger_auto_schema(
        tags=["criteria"],
        operation_description="It will return all criteria list",
    )

    def get(self, request):

        catagory_list= self.model.objects.filter(hide="no").order_by('-id')
        print(criteria_list)
        paginator = self.pagination_class
        page = paginator.paginate_queryset(criteria_list, request)
        serialized_data= self.serializer_class(page, many=True).data

        return Response({
            'status': 200,
            'catagory_list': serialized_data,
            'pagination_meta_data': paginator.pagination_meta_data(),

        })
