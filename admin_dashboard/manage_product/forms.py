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





# # =================================================== manage category  =============================================
class categoryEntryForm(forms.ModelForm):
    class Meta:
        model = common_models.Category
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
        fields = ['category', 'client', 'title', 'description', 'location', 'company_name', 'company_website', 'company_logo', 'vacancies', 'posted_at', 'expiry_date', 'job_type', 'status']
        widgets = {
            'posted_at': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

   
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(JobForm, self).__init__(*args, **kwargs)
        if self.user and not self.user.is_superuser:
            self.fields.pop('status')
            self.fields.pop('client')

def validate_contact(value):
    if len(str(value)) != 10 or not str(value).isdigit():
        raise ValidationError('Contact number must be exactly 10 digits and only contain numbers')


class ApplicationForm(forms.ModelForm):
    class Meta:
        model =common_models.Application
        fields = ['full_name','email','contact','resume']  
    full_name = forms.CharField(max_length=255)
    full_name.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})
    
    email = forms.EmailField(max_length=255)
    email.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Email',"required":"required"})

    contact = forms.IntegerField(
        validators=[validate_contact],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'maxlength': '10',
            'placeholder': 'Enter Mobile Number',
            'required': 'required'
        })
    )
    resume = forms.FileField(required=True)  # ImageField for uploading images
    resume.widget.attrs.update({'class': 'form-control'})

class EditUserForm(forms.Form):
    model =common_models.EditUser
    email = forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    full_name = forms.CharField(label="Full Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    contact = forms.IntegerField(label="Contact",widget=forms.NumberInput(attrs={"class":"form-control"}))



class AddUserForm(forms.ModelForm):
    class Meta:
        model = common_models.User
        fields = ['email', 'full_name','role', 'contact', 'password']  # Include necessary fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all fields as required
        for field in self.fields:
            self.fields[field].required = True

    # Optionally, customize validation or widgets
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    role = forms.ModelChoiceField(
        queryset=common_models.Job.objects.all(),  # Assuming Job model represents roles
        empty_label="Select a job role",  # Placeholder text for the dropdown
        widget=forms.Select(attrs={'class': 'form-control'}),  # Apply form-control class for styling
        required=True,  # Make the role field required explicitly
    )
    

class ClientForm(forms.ModelForm):

    class Meta:
        model = common_models.User
        fields = ['email', 'full_name', 'contact', 'password']

    password = forms.CharField(widget=forms.PasswordInput)


class CategoryFilterForm(forms.Form):
    model = common_models.Category
    category = forms.ModelChoiceField(queryset=model.objects.all(), required=True, label="Category")

class JobSelectionForm(forms.Form):
    model = common_models.Job
    jobs = forms.ModelMultipleChoiceField(queryset=model.objects.all(), required=True, widget=forms.CheckboxSelectMultiple, label="Select Jobs")

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category', None)
        super(JobSelectionForm, self).__init__(*args, **kwargs)
        if category:
            self.fields['jobs'].queryset = common_models.Job.objects.filter(category=category)



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = common_models.User
        fields = ['full_name', 'email', 'contact', 'category', 'wallet', 'token', 'meta_data']
        widgets = {
            'meta_data': forms.Textarea(attrs={'rows': 3}),
            'wallet': forms.NumberInput(attrs={'step': '0.01'}),
        }