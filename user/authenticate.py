from django.forms import ValidationError
from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import logout
from django.conf import settings
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from .forms import CustomPasswordResetForm,CustomSetPasswordForm
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator

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
            contact = form.cleaned_data.get('contact')
            pin = form.cleaned_data.get('pin')
            confirm_pin = form.cleaned_data.get('confirm_pin')
            full_name = form.cleaned_data.get('full_name')

            # Since we're now using a PIN, authenticate logic can be adjusted if needed
            user = auth.authenticate(request, username=contact, password=pin)
            if user is None:
                try:
                    if pin == confirm_pin:
                        new_user = self.model(contact=contact, full_name=full_name)
                        new_user.set_password(pin)  # Using PIN as the password

                        if email:
                            new_user.email = email  # Set email only if provided

                        try:
                            # If an email is provided, send an email confirmation
                            if email:
                                subject = "Registration Successful."
                                message = f"Dear {full_name}, your account has been created successfully. You can now log in."
                                from_email = "noreply@example.com"
                                send_mail(subject, message, from_email, [email], fail_silently=False)

                            new_user.save()
                            messages.success(request, 'Registration Successful! You can now log in.')
                            return redirect('user:login')
                        except Exception as e:
                            print("Error in sending verification mail", e)
                            messages.error(request, 'Error in sending email. Please try again later.')
                            return redirect('user:signup')
                    else:
                        messages.error(request, "PINs do not match.")
                except Exception as e:
                    print(e)
                    messages.error(request, 'Something went wrong during registration.')
            else:
                messages.error(request, "User already exists.")
        else:
            messages.error(request, "Please correct the errors below.")
        return render(request, self.template, {'form': form})

        
class Login(View):
    model = models.User
    template = app + "authtemp/login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template, {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data.get('identifier')
            password = form.cleaned_data.get('password')

            # Check if the identifier is an email or phone number
            if '@' in identifier:
                # If identifier contains '@', assume it's an email
                try:
                    user = self.model.objects.get(email=identifier)
                except self.model.DoesNotExist:
                    user = None
            else:
                # Otherwise, assume it's a phone number
                try:
                    user = self.model.objects.get(contact=identifier)
                except self.model.DoesNotExist:
                    user = None

            # Authenticate user
            if user is not None:
                authenticated_user = auth.authenticate(username=user.email, password=password)
                if authenticated_user is not None:
                    auth.login(request, authenticated_user)
                    if user.is_superuser:
                        return redirect('admin_dashboard:admin_dashboard')
                    else:
                        return redirect('user:home')
                else:
                    messages.error(request, "Incorrect password.")
            else:
                messages.error(request, "No user found with that email or phone number.")

        return render(request, self.template, {'form': form})


class Logout(View):
    def get(self, request, *args, **kwargs):
        
            if 'confirm' in request.GET:
                logout(request)
                return redirect('user:home')  # Redirect to home or appropriate page
            
            if 'cancel' in request.GET:
                if request.user.is_superuser:
                    return redirect('admin_dashboard:admin_dashboard')  # Redirect to the admin dashboard
                return redirect(request.META.get('HTTP_REFERER', 'user:home'))

            # Default redirect if neither confirm nor cancel
            return redirect('user:home')
        
       
    
class CustomPasswordResetView(FormView):
    template_name = app + "authtemp/password_reset.html"
    template_email = app + "authtemp/password_reset_email.html"

    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('user:password_reset_done')
    token_generator = default_token_generator

    def form_valid(self, form):
        email = form.cleaned_data['email']
        users = models.User._default_manager.filter(email=email)
        if users.exists():
            for user in users:
                current_site = get_current_site(self.request)
                mail_subject = 'Password reset link'
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = self.token_generator.make_token(user)
                reset_link = reverse_lazy('user:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                reset_url = f"{self.request.scheme}://{current_site.domain}{reset_link}"
                html_message = render_to_string(self.template_email, {
                    'user': user,
                    'reset_url': reset_url,
                })
                text_message = strip_tags(html_message)
                msg = EmailMultiAlternatives(mail_subject, text_message, 'admin@example.com', [email])
                msg.attach_alternative(html_message, "text/html")
                msg.send()
        return super().form_valid(form)
    
class CustomPasswordResetDoneView(TemplateView):
    template_name = app + "authtemp/password_reset_done.html"

UserModel = get_user_model()

class CustomPasswordResetConfirmView(FormView):
    template_name = app + "authtemp/password_reset_confirm.html"
    form_class = CustomSetPasswordForm
    token_generator = default_token_generator
    success_url = reverse_lazy('user:password_reset_complete')

    def dispatch(self, *args, **kwargs):
        self.user = self.get_user(kwargs['uidb64'])
        if self.user is not None and self.token_generator.check_token(self.user, kwargs['token']):
            return super().dispatch(*args, **kwargs)
        return self.render_to_response(self.get_context_data(validlink=False))

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            return UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['validlink'] = True if self.user is not None else False
        return context
    
class CustomPasswordResetCompleteView(TemplateView):
    template_name = app + "authtemp/password_reset_complete.html"