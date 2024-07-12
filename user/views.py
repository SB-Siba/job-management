from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.views import View
from django.contrib import messages
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# from app_common.models import Job, Application
from admin_dashboard.manage_product.forms import ApplicationForm ,CatagoryEntryForm
# from app_common.checkout.serializer import CartSerializer,DirectBuySerializer,TakeSubscriptionSerializer,OrderSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# from io import StringIO
from django.urls import reverse_lazy
from django.core.mail import send_mail
import json
# admin_dashboard/manage_product/user.py
from app_common.models import (
    Job,
    Catagory,
    UserProfile,
    User,
    Application,
    ContactMessage,
    
)

from helpers.utils import dict_filter,paginate # Import dict_filter function
import json

app = "user/"


class HomeView(View):
    template_client = app + 'client_home.html'
    template_user = app + 'home1.html'
    unauthenticated_template = app + 'home_for_landing.html'

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            jobs = Job.objects.all()
            print(jobs)
            return render(request, self.unauthenticated_template,locals())

        welcome_message = f"Welcome, {user.full_name}!"

        if user.is_staff:  # Check if user is marked as client (is_staff)
            # client = get_object_or_404(ClientProfile, user=user)  # Get the client profile
            # jobs = client.jobs.all()  # Assuming you have a related_name='jobs' in Client model
            # applications = Application.objects.filter(job__client=client)  # Adjust as per your Application model setup
            # context = {
            #     # 'client': client,
            #     'jobs': jobs,
            #     'applications': applications,
            #     'welcome_message': f"Welcome, {user.full_name}!"
            # }
            return render(request, self.template_client)

        # If user is authenticated but not a client, treat as candidate
        job_list = Job.objects.filter(expiry_date__gt=timezone.now()).order_by('-id')
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


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template = app + "userprofile.html"

    def get(self, request):
        user = request.user
        catagory_obj = Catagory.objects.all()
        print(catagory_obj)
        try:
            profile_obj = UserProfile.objects.get(user=user)
            # print(profile_obj,"hiehfipajdfpofj;ahfihiwfwkhw")
        except UserProfile.DoesNotExist:
            profile_obj = None

        return render(request, self.template, {'user': user, 'catagory_obj': catagory_obj, 'profile_obj': profile_obj})

@method_decorator(login_required, name='dispatch')
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

class Contact(View):
    template = app + "login"

    def get(self,request):
        return render(request,self.template)

class contactMesage(View):
    template = app + "contact_page.html"

    def get(self,request):
        initial = {'user': request.user.full_name}
        form = forms.ContactMessageForm(initial=initial)

        context={"form":form}
        return render(request,self.template,context)
    
    def post(self,request):
        form = forms.ContactMessageForm(request.POST)  # Instantiate the form with request POST data
        if form.is_valid():  # Add parentheses to is_valid()
            user = form.cleaned_data['user']
            query_message = form.cleaned_data['message']
            try:
                u_obj = get_object_or_404(User,full_name = user)
                user_email = u_obj.email
                subject = "Your Query Recived."
                message = f"Dear,\nYour Query has been recived successfully.\nOur Team members look into this."
                from_email = "forverify.noreply@gmail.com"
                send_mail(subject, message, from_email,[user_email], fail_silently=False)
                contact_obj = ContactMessage(user = u_obj,message =query_message)
                contact_obj.save()
                messages.info(request,"Your Message has been sent successfully.")
                return redirect("user:home")
            except Exception as e:
                print (e)
                messages.warning(request,"There was an error while sending your message.")
                return self.get(request)
        else:   # If the form is not valid, re-render the form with errors
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

    def get(self,request):
        return render(request,self.template)


@method_decorator(login_required, name='dispatch')
class PostJob(View):
    template_name = app + 'client/post_job.html'
    def get(self, request):
        form = JobForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.client = request.user
            job.save()
            messages.success(request, f'Job "{job.title}" posted successfully.')
            return redirect('client_job_list')
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class JobDetail(View):
    template_name = app + 'client/job_detail.html'
    
    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        if job.client != request.user:
            messages.error(request, "You do not have permission to view this job.")
            return redirect('client_job_list')
        context = {
            "job": job
        }
        return render(request, self.template_name, context)

class ThankYou(View):
    template = app + "thankyoupage.html"
    def get(self, request):
        return render(request, self.template)

