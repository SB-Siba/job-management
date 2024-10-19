from django import forms
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm,SetPasswordForm
from app_common import models as common_models
from django.contrib.auth import password_validation
from django.core.validators import RegexValidator


from django import forms
import re

class SignUpForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Full Name',
        max_length=100
    )
    
    email = forms.EmailField(
        max_length=254,
        required=False,  # Email is now optional
        help_text='Optional. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    contact = forms.CharField(
        max_length=15,  # Adjust based on expected phone number format
        help_text='Required. Enter a valid contact number.',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    pin = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),  # PIN is treated as a password input
        label='PIN',
        min_length=6,
        max_length=6,
        help_text='Enter a 6-digit PIN.',
    )
    
    confirm_pin = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm PIN',
    )

    def clean_pin(self):
        pin = self.cleaned_data.get('pin')
        # Validate that the PIN is numeric and has exactly 6 digits
        if not pin.isdigit():
            raise forms.ValidationError("PIN must contain only numeric digits.")
        if len(pin) != 6:
            raise forms.ValidationError("PIN must be exactly 6 digits.")
        return pin

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get("pin")
        confirm_pin = cleaned_data.get("confirm_pin")
        if pin and confirm_pin and pin != confirm_pin:
            raise forms.ValidationError("PINs doesn't match.")
        return cleaned_data

class LoginForm(forms.Form):
    identifier = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email or Phone Number'}),
        label="Email or Phone Number"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password"
    )
    
class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password',widget=forms.PasswordInput(attrs= {'autofocus':True,'autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label='New Password',widget=forms.PasswordInput(attrs= {'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Cofirm Password',widget=forms.PasswordInput(attrs= {'autocomplete':'current-password','class':'form-control'}))

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control text-black',
            'placeholder': 'Email Address'
        })
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class': 'form-control text-black'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class': 'form-control text-black'}),
        strip=False,
    )

class UpdateProfileForm(forms.Form):
    
    email = forms.EmailField(max_length=255)
    email.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Email',"required":"required"})

    full_name = forms.CharField(max_length=255)
    full_name.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Full Name',"required":"required"})

    contact = forms.CharField(
    validators=[RegexValidator(r'^\d{10}$', 'Contact number must be 10 digits')],
    widget=forms.TextInput(attrs={'type': 'number', 'max_length': 10, 'class': 'form-control'})
    )


    skills = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control","rows":"1"}))
    skills.widget.attrs.update({'class': 'form-control','type':'text'})

    # password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs= {'autocomplete':'current-password','class':'form-control','placeholder':'Only if you want to change then type here.'}),required=False)

    profile_pic = forms.FileField(label='Select Your Profile', required=False)
    profile_pic.widget.attrs.update({'class': 'form-control', 'type': 'file'})

    resume = forms.FileField(label='Select your Resume', required=False)
    resume.widget.attrs.update({'class': 'form-control', 'type': 'file'})

    category = forms.ModelChoiceField(queryset=common_models.Category.objects.all(), empty_label=None)  # Use your Property queryset here
    category.widget.attrs.update({'class': 'form-control', 'required': 'required'})

    

class ContactMessageForm(forms.Form):
    name = forms.CharField(
        max_length=255, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Name'}),
        label='Full Name'
    )
   
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email'}),
        required=True,
        label='Email'
    )
   
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Your Message'}),
        required=True,
        label='Message'
    )

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = common_models.Employee
        fields = ['salary', 'period_start', 'period_end']
        widgets = {
            'period_start': forms.SelectDateWidget(),
            'period_end': forms.SelectDateWidget(),
        }

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = common_models.Application
        fields = ['status']

class ReplaceEmployeeForm(forms.Form):
    application_id = forms.IntegerField(widget=forms.HiddenInput())
    email = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    new_employee_name = forms.CharField(max_length=100, required=True)
    new_employee_email = forms.EmailField(required=True)
    new_employee_phone = forms.CharField(max_length=10, min_length=10, required=True)

    def clean_new_employee_phone(self):
        phone = self.cleaned_data.get('new_employee_phone')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone