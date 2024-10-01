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
        help_text='Required. Inform a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    contact = forms.CharField(
        max_length=15,  # Adjust based on expected phone number format
        help_text='Required. Enter a valid contact number.',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password'
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm Password'
    )
    
    # Resume = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Password policy validation
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[\W_]', password):
            raise forms.ValidationError("Password must contain at least one special character.")
        if len(password) < 8 or len(password) > 14:
            raise forms.ValidationError("Password must be between 8 and 14 characters long.")
        if " " in password:
            raise forms.ValidationError("Password cannot contain spaces.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
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