from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.views import View
from django.contrib import messages
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from . import forms
from django.contrib.auth.decorators import login_required
from app_common.models import Job, Application
from admin_dashboard.manage_product.forms import ApplicationForm
# from app_common.checkout.serializer import CartSerializer,DirectBuySerializer,TakeSubscriptionSerializer,OrderSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# from io import StringIO
from django.core.mail import send_mail
import json
from app_common.models import (
    Job,
    Catagory,
    UserProfile,
    User,Application,
    
)

from helpers.utils import dict_filter  # Import dict_filter function
import json

app = "user/"


class HomeView(View):
    template = app + "home1.html"
    un_template = app + "landing_page.html"
    def get(self, request):
        user = request.user
        if not user.is_authenticated:

            return render(request, self.un_template, locals())

        return render(request, self.template, locals())


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
        category_obj = Category.objects.all()
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            full_name = form.cleaned_data["full_name"]
            contact = form.cleaned_data["contact"]
            skills = form.cleaned_data["skills"]
            profile_picture = form.cleaned_data["profile_pic"]
            password = form.cleaned_data["password"]
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


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def apply_for_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user
            application.save()
            return redirect('job_list')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_for_job.html', {'form': form, 'job': job})




    
class contactMesage(View):
    template = app + "contact_page.html"

    def get(self,request):
        # initial = {'user': request.user.full_name}
        form = forms.ContactMessageForm

        context={"form":form}
        return render(request,self.template,context)
    
    def post(self,request):
        form = forms.ContactMessageForm(request.POST)  # Instantiate the form with request POST data
        if form.is_valid():  # Add parentheses to is_valid()
            user = form.cleaned_data['user']
            email= form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                u_obj = get_object_or_404(User,full_name = user)
                user_email = u_obj.email
                subject = "Your Query Recived."
                message = f"Dear,\nYour Query has been recived successfully.\nOur Team members look into this."
                from_email = "noreplyf577@gmail.com"
                send_mail(subject, message, from_email,[user_email], fail_silently=False)
                contact_obj = ContactMessage(user = u_obj,message = message)
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
        
class ThankYou(View):
    template = app + "thankyoupage.html"
    def get(self, request):
        return render(request, self.template)

