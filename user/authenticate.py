from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from django.contrib import messages
from django.contrib import auth
from django.conf import settings
#import requests
from . forms import SignUpForm,LoginForm
from . import forms
from django.contrib.auth import logout
from helpers import privacy_t_and_c
from app_common import models
from app_common.models import User
from django.core.mail import send_mail


app = "user/"


class Registration(View):
    model = models.User
    template = app + "authtemp/registration.html"

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            full_name = form.cleaned_data.get('full_name')
            # resume = form.FileField('resume')

            user = auth.authenticate(request, username=email, password=password)
            if user is None:
                try:
                    if password == confirm_password:
                        new_user = self.model(email=email, full_name=full_name)
                        new_user.set_password(password)
                        try:
                            user_email = email
                            subject = "Registration Successfull."
                            message = f"""\
                            Dear {full_name},
                            Your account has been created successfully on our site. You can login now."""
                            from_email = "noreplyf577@gmail.com"
                            send_mail(subject, message, from_email,[user_email], fail_silently=False)

                            new_user.save()
                            messages.success(request, 'Registration Successful!')
                            return redirect('user:login')
                        except Exception as e:
                            print("Error in sending verfication mail",e)
                            messages.error(request,'Email could not be sent due to some error.Please contact support for further assistance.')
                            return redirect('user:signup')
                    else:
                        messages.error(request, "Password does not match with Confirm Password")
                        return redirect('user:signup')
                except Exception as e:
                    print(e)
                    messages.error(request, 'Something went wrong while registering your account. Please try again later.')
            else:
                messages.error(request, "User already exists.")
        return render(request, self.template, {'form': form})


        
class Login(View):
    model=models.User
    template = app + "authtemp/login.html"

    def get(self,request):
        form = LoginForm()
        print("hiii")
        return render(request, self.template, {'form': form})
    
    def post(self,request):
        print("byyy")
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
            print("hrbvhrwbrw")
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            user=auth.authenticate(username=email, password=password)
            print(user)
            if user is not None:      
                auth.login(request,user) 
                if user.is_superuser == True:
                    return redirect('admin_dashboard:admin_dashboard') 
                else:
                    return redirect('user:home')
            else:
                messages.error(request, "Login Failed")
        print("hhhh")
        return redirect('user:login')

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('user:login')

class ForgotPasswordView(View):
    template_name = app + 'authtemp/forgot_password.html'
 
    def get(self, request):
        form = forms.ForgotPasswordForm()
        return render(request, self.template_name, {'form': form})
 
    def post(self, request):
        form = forms.ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                user.send_reset_password_email()
                return HttpResponse("Password reset email sent successfully.")
            except User.DoesNotExist:
                return HttpResponse("No user found with this email address.")
            except Exception as e:
                return HttpResponse(f"An error occurred: {e}")
        return render(request, self.template_name, {'form': form})
   
   
   
   
class ResetPasswordView(View):
    template_name = app + 'authtemp/reset_password.html'
 
    def get(self, request, token):
        form = forms.ResetPasswordForm()
        return render(request, self.template_name, {'form': form})
 
    def post(self, request, token):
        form = forms.ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            if new_password != confirm_password:
                return HttpResponse("Passwords do not match.")
            try:
                user = User.objects.get(token=token)
                if user:
                    # Reset the password
                    user.set_password(new_password)
                    user.token = None  # Clear the token after password reset
                    user.save()
                    messages.success( request,"Password reset successfully.")
                    return redirect('user:login')
                else:
                    return HttpResponse("Invalid token.")
            except User.DoesNotExist:
                return HttpResponse("Invalid token.")
        return render(request, self.template_name, {'form': form})