from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from helpers import utils
from app_common.models import User

class UserCreateForm(forms.ModelForm):
    
    full_name = forms.CharField(max_length=255)
    full_name.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Name',"required":"required"})

    email = forms.CharField(max_length=255, label='Email')
    email.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Email',"required":"required"})

    contact = forms.IntegerField()
    contact.widget.attrs.update({'class': 'form-control','type':'number','placeholder':'Contact Number',"required":"required"})

    password = forms.CharField(initial="password",widget=forms.PasswordInput(attrs={'type':'password','class': 'form-control', 'value':'password'}))

    class Meta:
        model = User
        fields = ["full_name","email", "contact" ,"password"]