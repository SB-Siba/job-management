from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from admin_dashboard.manage_product import forms
from django.contrib import messages

from django.utils.decorators import method_decorator
from app_common import models as common_model
from . import forms
from helpers import utils
from django.http import JsonResponse
from django.contrib.auth.models import User
from admin_dashboard.manage_product import forms 
from django.urls import reverse_lazy


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
    form_class = forms.ClientForm
    
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

        job_data = []
        for job in jobs:
            applications_count = common_model.Application.objects.filter(job=job).count()
            hired_count = common_model.Application.objects.filter(job=job, status='Hired').count()
            job_data.append({
                'job': job,
                'applications_count': applications_count,
                'hired_count': hired_count,
            })

        context = {
            'client': client,
            'job_data': job_data,
        }
        return render(request, self.template_name, context)
    
# UpdateClientView for editing client details
class EditClientView(View):
    form_class = forms.ClientForm
    template_name = 'admin_dashboard/client_list.html'
    success_url = reverse_lazy('admin_dashboard:client_list')

    def get(self, request, pk):
        client = get_object_or_404(common_model.User, id=pk, is_staff=True, is_superuser=False)
        form = self.form_class(instance=client)
        return render(request, self.template_name, {'form': form, 'client': client})

    def post(self, request, pk):
        client = get_object_or_404(common_model.User, id=pk, is_staff=True, is_superuser=False)
        form = self.form_class(request.POST, instance=client)

        if form.is_valid():
            updated_client = form.save()

            if request.is_ajax():
                return JsonResponse({
                    'success': True,
                    'client': {
                        'id': updated_client.id,
                        'full_name': updated_client.get_full_name(),
                        'email': updated_client.email,
                        'contact': updated_client.contact,
                    },
                    'message': 'Client updated successfully.'
                })
            else:
                messages.success(request, 'Client updated successfully.')
                return redirect(self.success_url)
        else:
            if request.is_ajax():
                return JsonResponse({'success': False, 'errors': form.errors})
            else:
                messages.error(request, 'There was an error updating the client. Please check the details and try again.')
                return render(request, self.template_name, {'form': form, 'client': client})


# DeleteClientView for deleting a client
class DeleteClientView(View):
    def post(self, request, client_id):
        client = get_object_or_404(common_model.User, id=client_id, is_staff=True, is_superuser=False)
        client.delete()
        messages.success(request, 'Client deleted successfully.')
        return JsonResponse({'success': True, 'message': 'Client deleted successfully.'})

