from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from admin_dashboard.manage_product import forms
from django.contrib import messages

from django.utils.decorators import method_decorator
from app_common import models as common_model
from . import forms
from helpers import utils
from django.http import JsonResponse
from admin_dashboard.manage_product import forms 
from django.urls import reverse, reverse_lazy


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
class ClientUpdateView(View):
    template_name = 'admin_dashboard/manage_product/client_edit.html'

    def get(self, request, uid):
        client = get_object_or_404(common_model.User, pk=uid)
        form = forms.ClientUpdateForm(instance=client)
        context = {
            'form': form,
            'client_id': uid,
            'username': client.email,  # Or another field if needed
        }
        return render(request, self.template_name, context)

    def post(self, request, uid):
        client = get_object_or_404(common_model.User, pk=uid)
        form = forms.ClientUpdateForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client updated successfully.')
            return redirect('admin_dashboard:client_list')  # Redirect to the client list or detail view
        context = {
            'form': form,
            'client_id': uid,
            'username': client.email,  # Or another field if needed
        }
        return render(request, self.template_name, context)

# DeleteClientView for deleting a client
class DeleteClientView(View):
    template = app+ 'client_list.html'
    def post(self, request, client_id):
        client = get_object_or_404(common_model.User, id=client_id, is_staff=True, is_superuser=False)
        client.delete()
        messages.success(request, 'Client deleted successfully.')
        return redirect('admin_dashboard:client_list')

class ClientRequestView(View):
    template_name = app + 'client_request.html'
    
    def get(self, request, *args, **kwargs):
        # Fetch all employee replacement requests
        requests = common_model.EmployeeReplacementRequest.objects.all()
        for req in requests:
            print(req.client_email.email) 
        context = {
            'requests': requests
        }
        
        # Render the template with the context data
        return render(request, self.template_name, context)
    
class ProvideEmployeeView(View):
    template_name = app + 'provide_employee.html'

    def get(self, request, *args, **kwargs):
        client_id = kwargs.get('client_id', None)
        form = forms.ProvideEmployeeForm(client_id=client_id)

        # Get assigned employee ids for the specific client
        assigned_employee_ids = common_model.ClientEmployee.objects.filter(client_id=client_id).values_list('employee_id', flat=True)
        available_employees = common_model.Employee.objects.exclude(id__in=assigned_employee_ids)

        return render(request, self.template_name, {
            'form': form,
            'available_employees': available_employees,
        })

    def post(self, request, *args, **kwargs):
        form = forms.ProvideEmployeeForm(request.POST)

        if form.is_valid():
            client = form.cleaned_data['client']
            employees = form.cleaned_data['employees']

            assigned_employee_ids = []
            for employee in employees:
                client_employee, created = common_model.ClientEmployee.objects.get_or_create(client=client, employee=employee)
                if created:  # If a new assignment was created, store the ID
                    assigned_employee_ids.append(employee.id)

            messages.success(request, f'Employees successfully assigned to {client.full_name}.')
            return JsonResponse({'assigned_employee_ids': assigned_employee_ids})  # Return the IDs of assigned employees

        # If the form is invalid, re-render with the existing data
        assigned_employee_ids = common_model.ClientEmployee.objects.filter(client_id=client_id).values_list('employee_id', flat=True)
        available_employees = common_model.Employee.objects.exclude(id__in=assigned_employee_ids)

        return render(request, self.template_name, {
            'form': form,
            'available_employees': available_employees,
        })

class DeleteClientEmployeeView(View):
    """View to handle the deletion of a client-employee record."""
    
    def post(self, request, pk, *args, **kwargs):
        # Get the ClientEmployee instance by primary key (pk)
        client_employee = get_object_or_404(common_model.ClientEmployee, pk=pk)
        
        # Delete the record
        client_employee.delete()
        
        # Redirect back to the ProvideEmployee page after deletion
        return redirect(reverse('admin_dashboard:provide_employee'))
    
class ProvidedEmployeeListView(View):
    template_name = app + 'provided_employee_list.html'  # Adjust path as needed

    def get(self, request, *args, **kwargs):
        # Fetch all the client-employee assignments
        provided_employees = common_model.ClientEmployee.objects.select_related('client', 'employee').all()

        # Create context with provided employees
        context = {
            'provided_employees': provided_employees,
        }

        return render(request, self.template_name, context)
    
class ClientEmployeeDeleteView(View):
    model = common_model.ClientEmployee
    template_name = app + 'provided_employee_list.html' 
    success_url = reverse_lazy('admin_dashboard:provided_employee_list')

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model, pk=kwargs['pk'])
        self.object.delete()
        messages.success(request, 'Employee assignment deleted successfully.')
        return redirect(self.success_url)