from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from app_common import models as common_models

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
    template = "admin_dashboard/index.html"

    def get(self, request):
        total_employees = common_models.User.objects.filter(is_staff=True).count()
        total_clients = common_models.User.objects.filter(is_superuser=False).count()  # Assuming clients are not superusers
        total_jobs = common_models.Job.objects.count()
        total_candidates = common_models.User.objects.filter(is_staff=False).count()  # Assuming candidates are non-staff users

        # Count published and unpublished jobs
        published_jobs = common_models.Job.objects.filter(status='published').count()
        unpublished_jobs = common_models.Job.objects.filter(status='unpublished').count()

        context = {
            'total_employees': total_employees,
            'total_clients': total_clients,
            'total_jobs': total_jobs,
            'total_candidates': total_candidates,
            'job_count': total_jobs,
            'published_jobs': published_jobs,
            'unpublished_jobs': unpublished_jobs,
        }

        return render(request, self.template, context)
    
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
    
