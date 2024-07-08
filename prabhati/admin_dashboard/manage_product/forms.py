from django import forms
from helpers import utils
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.forms.utils import ValidationError
from django.forms.widgets import MultiWidget
from django.core.validators import RegexValidator

from app_common import models as common_models

class MaxFileSizeValidator:
    def __init__(self, max_size=50*1024):
        self.max_size = max_size

    def __call__(self, file):
        if file.size > self.max_size:
            raise ValidationError(f"For performence purpose file-size should not exceed {self.max_size/1024} KB.")





# # =================================================== manage catagory  =============================================
class CatagoryEntryForm(forms.ModelForm):
    class Meta:
        model = common_models.Catagory
        fields = [
            'title',
            'description',

        ]
    
    title = forms.CharField(max_length=255)
    title.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    description = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control","rows":"2"}))
    description.widget.attrs.update({'class': 'form-control','type':'text'})




class JobForm(forms.ModelForm):
    class Meta:
        model = common_models.Job
        fields = ['catagory','client','title','description','location','company_name','company_website','company_logo','vacancies','published', 'posted_at', 'expiry_date', 'job_type']
        widgets = {
            'posting_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'expiration_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model =common_models.Application
        fields = ['full_name','email','contact','resume']  
    full_name = forms.CharField(max_length=255)
    full_name.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})
    
    email = forms.EmailField(max_length=255)
    email.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Email',"required":"required"})

    contact = forms.CharField(max_length=15,validators=[RegexValidator(regex='^\d{10,15}$', message='Contact number must be between 10 and 15 digits')])
    contact.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Mobile Number',"required":"required"})

    resume = forms.FileField(required=False)  # ImageField for uploading images
    resume.widget.attrs.update({'class': 'form-control'})

class EditUserForm(forms.Form):
    model =common_models.Edit_User
    email = forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    full_name = forms.CharField(label="Full Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    contact = forms.CharField(max_length=15,validators=[RegexValidator(regex='^\d{10,15}$', message='Contact number must be between 10 and 15 digits')])



class AddUserForm(forms.ModelForm):
    class Meta:
        model = common_models.User
        fields = ['email', 'full_name', 'contact', 'password']  # Include necessary fields

    # Optionally, you can add custom validation or widgets
    password = forms.CharField(widget=forms.PasswordInput)

class ClientForm(forms.ModelForm):
    

    class Meta:
        model = common_models.User
        fields = ['email', 'full_name', 'contact', 'password']

    password = forms.CharField(widget=forms.PasswordInput)