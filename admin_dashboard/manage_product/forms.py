from django import forms
from helpers import utils
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.forms.utils import ValidationError
from django.forms.widgets import MultiWidget

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
        fields = [
            'title',
            'catagory',
            'description',
            'requirements',
            'location',
            'posted_at',

        ]
    
    title = forms.CharField(max_length=255)
    title.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    catagory = forms.ModelChoiceField(queryset = common_models.Catagory.objects.all())
    catagory.widget.attrs.update({'class': 'form-control','type':'text'})


    description = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","rows":"2"}))
    description.widget.attrs.update({'class': 'form-control','type':'text'})


    requirements = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","rows":"2"}))
    requirements.widget.attrs.update({'class': 'form-control','type':'text'})

    location = forms.CharField(max_length=255)
    location.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})


    posted_at = forms.DateField()
    posted_at.widget.attrs.update({'class': 'form-control','type':'date',"required":"required"})
    posted_at = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


   


class ApplicationForm(forms.Form):
    class Meta:
        model =common_models.Application
        fields = ['resume', 'user']  

class EditUserForm(forms.Form):
    model =common_models.Edit_User
    email = forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    full_name = forms.CharField(label="Full Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    contact = forms.IntegerField(label="Contact",widget=forms.NumberInput(attrs={"class":"form-control"}))

