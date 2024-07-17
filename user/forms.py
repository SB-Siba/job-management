from django import forms
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm,SetPasswordForm
from app_common import models as common_models
from django.contrib.auth import password_validation
from django.core.validators import RegexValidator
class SignUpForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # phone_number = forms.IntegerField(help_text='Required. Enter a valid contact number .',
    #                          widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # Resume=forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))



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

    contact = forms.IntegerField()
    contact.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Mobile Number',"required":"required"})

    skills = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control","rows":"1"}))
    skills.widget.attrs.update({'class': 'form-control','type':'text'})

    # password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs= {'autocomplete':'current-password','class':'form-control','placeholder':'Only if you want to change then type here.'}),required=False)

    profile_pic = forms.FileField(label='Select Your Profile', required=False)
    profile_pic.widget.attrs.update({'class': 'form-control', 'type': 'file'})

    resume = forms.FileField(label='Select your Resume', required=False)
    resume.widget.attrs.update({'class': 'form-control', 'type': 'file'})

    catagory = forms.ModelChoiceField(queryset=common_models.Catagory.objects.all(), empty_label=None)  # Use your Property queryset here
    catagory.widget.attrs.update({'class': 'form-control', 'required': 'required'})

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
        fields = ['salary', 'period_start', 'period_end', 'docs']
        widgets = {
            'period_start': forms.DateInput(attrs={'type': 'date'}),
            'period_end': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'salary': 'Salary',
            'period_start': 'Period Start',
            'period_end': 'Period End',
            'docs': 'Documents',
        }

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = common_models.Application
        fields = ['status']