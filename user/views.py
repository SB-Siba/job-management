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
    template = app + "home1.html"
    un_template = app + "landing_page.html"

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return render(request, self.un_template, locals())

        job_list = Job.objects.filter(published=True, expiry_date__gt=timezone.now()).order_by('-uid')
        paginated_data = paginate(request, job_list, 50)
        form = ApplicationForm()  # This form will be used for the application modal/form
        context = {
            "job_list": job_list,
            "data_list": paginated_data,
            "form": form
        }

        return render(request, self.template, context)


class ProfileView(View):
    template = app + "userprofile.html"

    def get(self, request):
        user = request.user
        print(user)
        catagory_obj =Catagory.objects.all()
        userobj = User.objects.get(email=user.email)

        try:
            profileobj = UserProfile.objects.get(user=userobj)
        except UserProfile.DoesNotExist:
            profileobj = None


        if not user.is_authenticated:
            return redirect("user:login")

        return render(request, self.template, locals())


class UpdateProfileView(View):
    template = app + "update_profile.html"
    form = forms.UpdateProfileForm

    def get(self, request):
        user = request.user
        catagory_obj = Catagory.objects.all()
        userobj = User.objects.get(email=user.email)
        print(userobj)
    
        profileObj, created = UserProfile.objects.get_or_create(user=userobj)
       
        # print(profileObj)
        initial_data = {
            "email": userobj.email,
            "full_name": userobj.full_name,
            "contact": userobj.contact,
            "skills": profileObj.skills,
            "profile_pic": profileObj.profile_pic,
            "Resume": profileObj.resume,
        }
        form = self.form(initial=initial_data)

        return render(request, self.template, locals())

    def post(self, request):
        catagory_obj = Catagory.objects.all()
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            full_name = form.cleaned_data["full_name"]
            contact = form.cleaned_data["contact"]
            skills = form.cleaned_data["skills"]
            profile_picture = form.cleaned_data["profile_pic"]
            # password = form.cleaned_data["password"]
            resume = form.cleaned_data["resume"]

            user = request.user

            try:
                userobj = User.objects.get(email=user.email)
                userobj.email = email
                userobj.full_name = full_name
                userobj.contact = contact
                profile_object = UserProfile.objects.filter(user=user)

                if profile_picture is None:
                    picture = ""
                    for i in profile_object:
                        picture = i.profile_pic
                else:
                    picture = profile_picture

                if len(profile_object) == 0:
                    profileobj = UserProfile(user=user, skills=skills, profile_pic=picture)
                    profileobj.save()
                else:
                    for i in profile_object:
                        i.user = user
                        i.profile_pic = picture
                        i.skills = skills
                        i.save()

                
                        
                if len(password) > 6:
                    userobj.set_password(password)
                    messages.success(request, "Password Changed Successfully")

                userobj.save()
                return redirect("user:account_details")

            except:
                messages.error(request, "Error in Updating Profile")
        return render(request, self.template, locals())


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
        if filter_by == "category":
            category_id = request.GET.get("catagory_id")
            job_list = self.Job.objects.filter(category_id=category_id, published=True, expiry_date__gt=timezone.now()).order_by('-id')
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

class ApplicationSuccess(View):
    template = "user/application_success.html"

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
                return redirect("shoppingsite:home")
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


class AccountDetails(View):
    template = app + "accountdetails.html"

    def get(self,request):
        user = request.user
        catagory_obj = Catagory.objects.all()
        userobj = User.objects.get(id=user.id)
        try:
            profileobj = UserProfile.objects.get(user=userobj)
        except UserProfile.DoesNotExist:
            profileobj = None

        if not user.is_authenticated:
            return redirect("user:login")
        
        return render(request,self.template,locals())
    

class Sector(View):
    template = "user/sector.html"

    def get(self,request):
        return render(request,self.template)


class JobOpening(View):
    template = "user/job_opening.html"

    def get(self,request):
        return render(request,self.template)


class ThankYou(View):
    template = app + "thankyoupage.html"
    def get(self, request):
        return render(request, self.template)

