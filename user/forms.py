from django import forms
from django.contrib.auth.forms import PasswordChangeForm,UserCreationForm
from app_common import models as common_models
from app_common.models import User
class SignUpForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.IntegerField(help_text='Required. Enter a valid contact number .',
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
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

    profile_pic = forms.FileField(label='Select a profile picture', required=False)
    profile_pic.widget.attrs.update({'class': 'form-control', 'type': 'file'})

    resume = forms.FileField(label='Select a resume', required=False)
    resume.widget.attrs.update({'class': 'form-control', 'type': 'file'})
    


class ContactMessageForm(forms.Form):

    user = forms.CharField(max_length=100, required=True)
    user.widget.attrs.update({'class': 'form-control','type':'text'})

    email = forms.EmailField(required=True)
    email.widget.attrs.update({'class': 'form-control','type':'text'})

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter Your Message'
        }),
        required=True
    )

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
 
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user found with this email address.")
        return email
   
   
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
 
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
