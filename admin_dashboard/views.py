from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
# -------------------------------------------- custom import


#import requests
from app_common.models import Order
from django.db.models import Count, Sum
from django.core.files.storage import default_storage

from helpers import utils, api_permission, privacy_t_and_c
from . import swagger_doc

from app_common import models as common_models
# from .forms import BannerForm
# from .serializer import BannerSerializer

app = "admin_dashboard/"

@method_decorator(utils.super_admin_only, name='dispatch')
class AdminDashboard(View):
    template = app + "index.html"

    def get(self, request):
        order= {}
        
        order_counts = Order.objects.values('order_status').annotate(
            count=Count('order_status'),
            total_order_value=Sum('order_value')
        ).order_by('order_status')

        # print(order_counts)
        for data in order_counts:
            order[data['order_status']] = data
        
        context = {
            "order": order,
        }
        return render(request, self.template, context)
    

    
# @method_decorator(utils.super_admin_only, name='dispatch')
# class BannerList(View):
#     template = app + "banner.html"
#     model = common_models.Banner
#     form_class = BannerForm

#     def get(self, request):
#         banner_list = self.model.objects.all().order_by('-id')
#         context={
#             "banner_list":banner_list,
#             "form":self.form_class,
#         }
#         return render(request, self.template, context)

#     def post(self, request):
#         form = self.form_class(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Banner is added...")
#         else:

#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request,f'{field}: {error}')
        
#         return redirect('admin_dashboard:web_banner_list')
    


# @method_decorator(utils.super_admin_only, name='dispatch')
# class BannerDelete(View):
#     model = common_models.Banner

#     def get(self, request, banner_id):
#         banner = self.model.objects.get(id= banner_id)
#         if banner.image:
#             image_path = banner.image.path
#             default_storage.delete(image_path)
#             banner.image = None
        
#         banner.delete()
#         messages.info(request, 'Image is deleted successfully....')

#         return redirect('admin_dashboard:web_banner_list')
    

# class ApiBannerList(APIView):
#     permission_classes = [api_permission.is_authenticated]
#     serializer_class= BannerSerializer
#     model= common_models.Banner

#     @swagger_auto_schema(
#         tags=["banner"],
#         operation_description="Banner List API",
#     )
#     def get(self,request ):
        
#         banner_list = self.model.objects.filter(show="yes").order_by('sl_no')
#         return Response({
#             'status':200,
#             "banner_list": self.serializer_class(banner_list, many=True).data
        # })
    


# ===================================== privacy policy and t&c & about
class ApiPrivacyPolicy(APIView):
    permission_classes = [api_permission.is_authenticated]

    @swagger_auto_schema(
        tags=["privacy policy and t&c & about"],
        operation_description="Privacy Policy",
    )
    def get(self,request ):
        
        return Response({
            'status':200,
            "data": privacy_t_and_c.privacy_policy or None
        })
    
class ApiTermsCondition(APIView):
    permission_classes = [api_permission.is_authenticated]

    @swagger_auto_schema(
        tags=["privacy policy and t&c & about"],
        operation_description="Terms and Condition",
    )
    def get(self,request ):
        
        return Response({
            'status':200,
            "data": privacy_t_and_c.t_and_c or None
        })

class ApiAbountUs(APIView):
    permission_classes = [api_permission.is_authenticated]

    @swagger_auto_schema(
        tags=["privacy policy and t&c & about"],
        operation_description="About Us",
    )
    def get(self,request ):
        
        return Response({
            'status':200,
            "data": privacy_t_and_c.about_us or None
        })
    
