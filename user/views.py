from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.http import HttpResponseBadRequest
from django.views import View
from django.contrib import messages
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# from app_common.models import Job, Application
from admin_dashboard.manage_product.forms import ApplicationForm ,CatagoryEntryForm , JobForm
# from app_common.checkout.serializer import CartSerializer,DirectBuySerializer,TakeSubscriptionSerializer,OrderSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# from io import StringIO
from django.urls import reverse_lazy
from django.core.mail import send_mail
import json
import random
import string

# admin_dashboard/manage_product/user.py
from app_common.models import (
    Job,
    Catagory,
    UserProfile,
    User,
    Application,
    ContactMessage,
    Employee,
    
)

from helpers.utils import dict_filter,paginate # Import dict_filter function
import json

app = "user/"


class HomeView(View):
    template_client = app + 'client_home.html'
    template_user = app + 'home1.html'
    template_user = app + 'home1.html'
    unauthenticated_template = app + 'home_for_landing.html'
 
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            jobs = Job.objects.all()
            return render(request, self.unauthenticated_template, {'jobs': jobs})

        welcome_message = f"Welcome, {user.full_name}!"
 
        if user.is_staff:  # Check if user is marked as client (is_staff)
            jobs = Job.objects.filter(client=user).order_by('-posted_at')
            context = {
                'jobs': jobs,
                'welcome_message': welcome_message,
            }
            return render(request, self.template_client, context)

        # If user is authenticated but not a client, treat as candidate
        job_list = Job.objects.filter(status='published', expiry_date__gt=timezone.now()).order_by('-published_date')
        if user.catagory:
            job_list = job_list.filter(catagory=user.catagory)
        paginated_data = paginate(request, job_list, 50)
        form = ApplicationForm()  # This form will be used for the application modal/form
        context = {
            "job_list": job_list,
            "data_list": paginated_data,
            "form": form,
        }
 
        return render(request, self.template_user, context)


class ProfileView(View):
    template = app + "userprofile.html"

    def get(self, request):
        user = request.user
        catagory_obj = Catagory.objects.all()
        print(catagory_obj)
        try:
            profile_obj = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile_obj = None

        return render(request, self.template, {'user': user, 'catagory_obj': catagory_obj, 'profile_obj': profile_obj})

class UpdateProfileView(View):
    template = "user/update_profile.html"
    form_class = forms.UpdateProfileForm

    def get(self, request):
        user = request.user
        catagory_obj = Catagory.objects.all()
        try:
            profile_obj = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile_obj = None

        initial_data = {
            "email": user.email,
            "full_name": user.full_name,
            "contact": user.contact,
            "skills": profile_obj.skills if profile_obj else '',
            "profile_pic": profile_obj.profile_pic if profile_obj else None,
            "resume": profile_obj.resume if profile_obj else None,
            "catagory": user.catagory  # Assuming 'category' field in User model
        }
        form = self.form_class(initial=initial_data)

        return render(request, self.template, {'form': form, 'catagory_obj': catagory_obj})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            full_name = form.cleaned_data["full_name"]
            contact = form.cleaned_data["contact"]
            skills = form.cleaned_data["skills"]
            profile_picture = form.cleaned_data["profile_pic"]
            resume = form.cleaned_data["resume"]
            catagory = form.cleaned_data["catagory"]

            user = request.user

            try:
                user_obj = User.objects.get(email=user.email)
                user_obj.email = email
                user_obj.full_name = full_name
                user_obj.contact = contact
                user_obj.catagory = catagory  # Update category
                user_obj.save()

                profile_obj, created = UserProfile.objects.get_or_create(user=user_obj)
                profile_obj.skills = skills
                if profile_picture:
                    profile_obj.profile_pic = profile_picture
                if resume:
                    profile_obj.resume = resume
                profile_obj.save()

                return redirect("user:profile")

            except Exception as e:
                print(e)
                # Handle error messages or logging here if needed

        catagory_obj = Catagory.objects.all()
        print(catagory_obj)
        return render(request, self.template, {'form': form, 'catagory_obj': catagory_obj})

class UserJobSearch(View):
    form=CatagoryEntryForm()
    template = app + "jobs/job_list.html"

    def post(self, request):
        filter_by = request.POST.get("filter_by")
        query = request.POST.get("query")
        if filter_by == "uid":
            job_list = self.Job.objects.filter(id=query, published=True, expiry_date__gt=timezone.now())
        else:
            job_list = self.Job.objects.filter(title__icontains=query, published=True, expiry_date__gt=timezone.now())

        paginated_data = utils.paginate(request, job_list, 50)
        context = {
            "form": self.form_class,
            "job_list": job_list,
            "data_list": paginated_data
        }
        return render(request, self.template, context)
    

class UserJobFilter(View):
    template = app + "jobs/job_list.html"

    def get(self, request):
        filter_by = request.GET.get("filter_by")
        if filter_by == "catagory":
            catagory_id = request.GET.get("catagory_id")
            job_list = self.Job.objects.filter(catagory_id=catagory_id, published=True, expiry_date__gt=timezone.now()).order_by('-id')
        else:
            job_list = self.Job.objects.filter(published=True, expiry_date__gt=timezone.now()).order_by('-id')

        paginated_data = utils.paginate(request, job_list, 50)
        context = {
            "job_list": job_list,
            "data_list": paginated_data
        }
        return render(request, self.template, context)



class ApplyForJobView(View):
    template = app + 'job_apply.html'
    model = Application
    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        form = ApplicationForm()
        return render(request, self.template, {'job': job, 'form': form})

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        form = ApplicationForm(request.POST, request.FILES)
        resume = request.POST['resume']
        full_name = request.POST['full_name']
        email = request.POST['email']
        contact = request.POST['contact']
        applied_obj = self.model(job = job,email = email,user = request.user,contact = contact,resume = resume)
        applied_obj.save()
        
        return redirect('user:home')  # Redirect back to the job list view



@method_decorator(login_required, name='dispatch')
class AppliedJobsView(View):
    template_name = app + 'jobs/applied_jobs.html'

    def get(self, request):
        applied_jobs = Application.objects.filter(user=request.user)
        return render(request, self.template_name, {'applied_jobs': applied_jobs})
    def post(self, request):
       
        return redirect('user:applied_jobs')
class ApplicationSuccess(View):
    template = "user/application_success.html"

    def get(self,request):
        return render(request,self.template)

def get_rand_number(length=5):
    return ''.join(random.choices(string.digits, k=length))
class contactMesage(View):
    template = app + "contact_page.html"
 
    def get(self, request):
        if request.user.is_authenticated:
            initial = {'user': request.user.full_name , 'email': request.user.email}
            template = app + "contact_page.html"    
        else:
            initial = {}
            template = app + "contact_page_unauthenticated.html"
 
        form = forms.ContactMessageForm(initial=initial)
        context = {"form": form}
        return render(request, template, context)
 
    def post(self, request):
        form = forms.ContactMessageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            name = form.cleaned_data.get('name')
            email = form.cleaned_data['email']
            query_message = form.cleaned_data['message']
            try:
                if request.user.is_authenticated:
                    u_obj = request.user
                    contact_obj = ContactMessage(user=u_obj, message=query_message)
                else:
                    contact_obj = ContactMessage(uid=get_rand_number(5), message=query_message, reply=email)

                contact_obj.save()
 
                subject = "Your Query Received."
                message = f"Dear {name or email},\nYour query has been received successfully.\nOur team members will look into this."
                message = f"Dear {name or email},\nYour query has been received successfully.\nOur team members will look into this."
                from_email = "forverify.noreply@gmail.com"
                send_mail(subject, message, from_email, [email], fail_silently=False)
 
                if request.user.is_authenticated:
                    messages.info(request, "Your message has been sent successfully.")
                else:
                    messages.info(request, "Your message has been received. You can log in to track the response.")
               
                return redirect("user:contactmessage")
            except Exception as e:
                print(f"Exception: {e}")
                print(f"Exception: {e}")
                messages.warning(request, "There was an error while sending your message.")
                return self.get(request)
                return self.get(request)
        else:
            # Print form errors to the console for debugging
            print(f"Form errors: {form.errors}")
            # Print form errors to the console for debugging
            print(f"Form errors: {form.errors}")
            messages.warning(request, "Invalid form data. Please correct the errors.")
            return self.get(request)
       
     
        
     

class AboutPage(View):
    template = app + "about.html"

    def get(self,request):
        
        return render(request,self.template)


# class AccountDetails(View):
#     template = app + "accountdetails.html"

#     def get(self,request):
#         user = request.user
#         catagory_obj = Catagory.objects.all()
#         userobj = User.objects.get(id=user.id)
#         try:
#             profileobj = UserProfile.objects.get(user=userobj)
#         except UserProfile.DoesNotExist:
#             profileobj = None

#         if not user.is_authenticated:
#             return redirect("user:login")
        
#         return render(request,self.template,locals())
    

class Sector(View):
    template = "user/sector.html"

    def get(self,request):
        return render(request,self.template)


class JobOpening(View):
    template = "user/job_opening.html"
    model = Job
    def get(self, request):
        jobs = Job.objects.filter(status='published')
        return render(request, self.template, {'jobs': jobs})

# client 
@method_decorator(login_required, name='dispatch')
class PostJob(View):
    template_name = app + 'client/post_job.html'

    def get(self, request):
        form = JobForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = JobForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            job = form.save(commit=False)
            job.client = request.user
            job.save()
            messages.success(request, 'Job added successfully.')
            return redirect('user:job_list')
        return render(request, self.template_name, {'form': form})


class ClientJobEditView(View):
    template_name = 'job_form.html'

    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        if job.client != request.user:
            return redirect('client_job_list')
        form = JobForm(instance=job, user=request.user)
        return render(request, self.template_name, {'form': form, 'job': job})

    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        if job.client != request.user:
            return redirect('client_job_list')
        form = JobForm(request.POST, request.FILES, instance=job, user=request.user)
        if form.is_valid():
            job = form.save(commit=False)
            job.save()
            messages.success(request, f'Job "{job.title}" updated successfully.')
            return redirect('client_job_list')
        return render(request, self.template_name, {'form': form, 'job': job})


class ClientJobList(View):
    template_name = app + 'client/job_list.html'
    
    def get(self, request):
        job_list = Job.objects.filter(client=request.user).order_by('-id')
        paginated_data = paginate(request, job_list, 50)
        context = {
            "job_list": job_list,
            "data_list": paginated_data
        }
        return render(request, self.template_name, context)


class JobDetail(View):
    template_name = app + 'client/job_detail.html'
    
    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        employees = Employee.objects.filter(job=job)
        applications = Application.objects.filter(job=job)
        employee_form = forms.EmployeeForm()
        status_form = forms.ApplicationStatusForm()
        return render(request, self.template_name, {
            'job': job,
            'employees': employees,
            'applications': applications,
            'employee_form': employee_form,
            'status_form': status_form,
        })

    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)

        if 'employee_form' in request.POST:
            employee_id = request.POST.get('employee_id')
            employee = get_object_or_404(Employee, id=employee_id)
            form = forms.EmployeeForm(request.POST, instance=employee)
            if form.is_valid():
                updated_employee = form.save(commit=False)
                updated_employee.user = employee.user  # Ensure the user field is not set to NULL
                updated_employee.employer = employee.employer  # Ensure the employer field is not set to NULL
                updated_employee.job = job  # Ensure the job field is not set to NULL
                updated_employee.save()
                return redirect('user:job_detail', job_id=job.id)

        elif 'status_form' in request.POST:
            application_id = request.POST.get('application_id')
            status = request.POST.get('status')
            if not status:
                return HttpResponseBadRequest("Status field is required.")

            application = get_object_or_404(Application, id=application_id)
            application.status = status
            application.save()

            if status == 'Hired':
                # Assuming 'salary', 'period_start', 'period_end' are passed in POST data
                Employee.objects.create(
                    user=application.user,
                    job=application.job,
                    employer=request.user,
                    salary=request.POST.get('salary'),
                    period_start=request.POST.get('period_start'),
                    period_end=request.POST.get('period_end'),
                )
            elif status == 'Rejected':
                # Send rejection email
                send_mail(
                    'Job Application Status',
                    'Dear {},\n\nWe regret to inform you that your application for the position of {} at {} has been rejected.'.format(application.user.full_name, application.job.title, application.job.company_name),
                    'your-email@example.com',
                    [application.email],
                    fail_silently=False,
                )
            return redirect('user:job_detail', job_id=job.id)

        # If no form is submitted or there's an error, reload data for the GET request
        employees = Employee.objects.filter(job=job)
        applications = Application.objects.filter(job=job)
        employee_form = forms.EmployeeForm()
        status_form = forms.ApplicationStatusForm()
        return render(request, self.template_name, {
            'job': job,
            'employees': employees,
            'applications': applications,
            'employee_form': employee_form,
            'status_form': status_form,
        })



class ApplicationList(View):
    template_name = app + "client/application_list.html"

    def get(self, request, job_id):
        applications = Application.objects.filter(job_id=job_id)
        return render(request, self.template_name, {'applications': applications})

    def post(self, request, job_id):
        application_id = request.POST.get('application_id')
        status = request.POST.get('status')
        application = get_object_or_404(Application, id=application_id)

        if status == 'Hired':
            form = forms.EmployeeForm(request.POST)
            if form.is_valid():
                Employee.objects.create(
                    user=application.user,
                    job=application.job,
                    employer=request.user,  # assuming the logged-in user is the employer
                    salary=form.cleaned_data['salary'],
                    period_start=form.cleaned_data['period_start'],
                    period_end=form.cleaned_data['period_end'],
                )
            else:
                applications = Application.objects.filter(job_id=job_id)
                return render(request, self.template_name, {'applications': applications, 'form': form})

        application.status = status
        application.save()
        return redirect('user:application_list', job_id=job_id)

class EmployeeList(View): 
    template_name = app + "client/employee_list.html"

    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id, client=request.user)
        employees = Employee.objects.filter(application__job=job)
        context = {
            "job": job,
            "employees": employees,
        }
        return render(request, self.template_name, context)




class EmployeeListOverview(View):
    template_name = app + 'client/employee_list_overview.html'

    def get(self, request):
        if request.user.is_superuser:
            employees = Employee.objects.all()
        else:
            jobs = Job.objects.filter(client=request.user)
            employees = Employee.objects.filter(application__job__in=jobs)
        
        context = {
            'employees': employees
        }
        return render(request, self.template_name, context)



class EmployeeDetail(View):
    template_name = app + "client/employee_detail.html"

    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        context = {'employee': employee}
        return render(request, self.template_name, context)


class EmployeeUpdate(View):
    template_name = app + "client/employee_update.html"

    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        form = forms.EmployeeForm(instance=employee)
        context = {'form': form, 'employee': employee}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        form = forms.EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect(reverse('user:employee_detail', args=[pk]))
        context = {'form': form, 'employee': employee}
        return render(request, self.template_name, context)

class ThankYou(View):
    template = app + "thankyoupage.html"
    def get(self, request):
        return render(request, self.template)