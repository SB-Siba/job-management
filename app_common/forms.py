from django import forms
from helpers import utils
from django.forms.utils import ValidationError

from app_common import models as common_models

class NewPasswordForm(forms.Form):

    password1 = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput)
    password1.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Password',"required":"required"})

    password2 = forms.CharField(max_length=255,required=True)
    password2.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Confirm Password',"required":"required"})

    def clean(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError("Your password is not same..")
        
        if len(self.cleaned_data['password2']) < 5:
            raise forms.ValidationError("Your password is very weak ..")