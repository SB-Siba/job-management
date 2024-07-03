from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
# -------------------------------------------- custom import




from helpers import utils, api_permission, privacy_t_and_c
from . import swagger_doc

from app_common import models as common_models


app = "admin_dashboard/"

@method_decorator(utils.super_admin_only, name='dispatch')
class AdminDashboard(View):
    template = app + "index.html"

    def get(self, request):
        return render(request, self.template)
    

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
    
