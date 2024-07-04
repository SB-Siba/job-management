from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from admin_dashboard.manage_product import forms
from django.contrib import messages

from django.utils.decorators import method_decorator
from app_common import models as common_model
from . import forms
from helpers import utils


app = "admin_dashboard/manage_product/"


def is_admin(user):
    return user.is_staff

@method_decorator(utils.super_admin_only, name='dispatch')
class AdminClientListView(View):
    template = app + "client_list.html"
    def get(self, request):
        clients = common_model.User.objects.filter(is_staff=True, is_superuser=False)
        return render(request, self.template, {'clients': clients})
       

@method_decorator(utils.super_admin_only, name='dispatch')
class AdminClientCreateView(View):
    
    template = app + "client_form.html"
    form_class = forms. ClientForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.is_staff = True  # Mark as client
            client.set_password(form.cleaned_data['password'])
            client.save()
            messages.success(request, 'Client has been successfully added.')
            return redirect('admin_dashboard:client_list')
        else:
            messages.error(request, 'There was an error adding the client. Please check the details and try again.')
            return render(request, self.template, {'form': form})


@method_decorator(utils.super_admin_only, name='dispatch')
class ClientDetailView(View):
    template_name = app + 'client_detail.html'

    def get(self, request, client_id):
        client = get_object_or_404(common_model.User, id=client_id, is_staff=True, is_superuser=False)
        jobs = common_model.Job.objects.filter(client=client)

        total_applications = 0
        total_employees = 0
        for job in jobs:
            applications_count = common_model.Application.objects.filter(job=job).count()
            hired_count = common_model.Application.objects.filter(job=job, status='Hired').count()
            total_applications += applications_count
            total_employees += hired_count

        context = {
            'client': client,
            'jobs': jobs,
            'total_applications': total_applications,
            'total_employees': total_employees,
        }
        return render(request, self.template_name, context)