from django import forms
from helpers import utils
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.forms.utils import ValidationError
from django.forms.widgets import MultiWidget
from django.core.validators import RegexValidator
from ckeditor.widgets import CKEditorWidget
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

class sectorEntryForm(forms.ModelForm):
    class Meta:
        model = common_models.Sector
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
            'category', 'sector', 'title', 'description', 'location',
            'company_name', 'company_website', 'company_logo',
            'vacancies', 'posted_at', 'expiry_date', 'job_type', 'status'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'sector': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control', 'placeholder': 'Enter content'})),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'company_website': forms.URLInput(attrs={'class': 'form-control'}),
            'company_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'vacancies': forms.NumberInput(attrs={'class': 'form-control'}),
            'posted_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(JobForm, self).__init__(*args, **kwargs)

        self.fields['sector'].queryset = common_models.Sector.objects.all()

        self.fields['company_name'].initial = 'PRAVATI INTERNATIONAL SERVICE'
        self.fields['company_name'].widget.attrs['readonly'] = True

        # Set all fields to be required
        for field in self.fields:
            self.fields[field].required = True

        if self.user and not self.user.is_superuser:
            self.fields.pop('status')

def validate_contact(value):
    if len(str(value)) != 10 or not str(value).isdigit():
        raise ValidationError('Contact number must be exactly 10 digits and only contain numbers')

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = common_models.Application
        fields = ['full_name', 'email', 'contact', 'user_resume']  

    full_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
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
    user_resume = forms.FileField(required=True)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ApplicationForm, self).__init__(*args, **kwargs)

        if user is not None:
            # Ensure that user.full_name is a string, not a method
            self.fields['full_name'].initial = user.full_name
            self.fields['email'].initial = user.email
            self.fields['contact'].initial = user.contact
            self.fields['full_name'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True

        self.fields['full_name'].widget.attrs.update({'class': 'form-control', 'type': 'text', 'placeholder': 'Full name', "required": "required"})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'type': 'text', 'placeholder': 'Enter Email', "required": "required"})
        self.fields['user_resume'].widget.attrs.update({'class': 'form-control'})

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
        fields = ['full_name', 'email', 'contact', 'category', 'resume']

class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = common_models.User
        fields = ['full_name', 'email', 'contact']  # Include the fields you want to update
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
        }

class ProvideEmployeeForm(forms.Form):
    client = forms.ModelChoiceField(
        queryset=common_models.User.objects.filter(is_staff=True, is_superuser=False),
        label="Choose Client",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    employees = forms.ModelMultipleChoiceField(
        queryset=common_models.Employee.objects.filter(application__status='Hired').distinct(),
        label="Choose Employees",
        widget=forms.CheckboxSelectMultiple()
    )

    def __init__(self, *args, **kwargs):
        client_id = kwargs.pop('client_id', None)
        super(ProvideEmployeeForm, self).__init__(*args, **kwargs)

        # If a client is selected, adjust the employees queryset
        if client_id:
            assigned_employees = common_models.ClientEmployee.objects.filter(client_id=client_id).values_list('employee_id', flat=True)
            self.fields['employees'].queryset = common_models.Employee.objects.filter(
                application__status='Hired'
            ).exclude(id__in=assigned_employees).distinct()
        else:
            # Ensure it shows all available employees if no client is selected
            self.fields['employees'].queryset = common_models.Employee.objects.filter(
                application__status='Hired'
            ).distinct()

class EmployeeForm(forms.ModelForm):
    user_full_name = forms.CharField(max_length=255, label='Full Name', required=False)
    user_email = forms.EmailField(label='Email', required=False)
    contact = forms.CharField(max_length=15, label='Phone Number', required=False)

    period_start = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Start Period'
    )
    period_end = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='End Period'
    )

    class Meta:
        model = common_models.Employee
        fields = ['salary', 'period_start', 'period_end', 'docs']  # Exclude user from being editable
        widgets = {
            'user': forms.HiddenInput(),  # Hide user field from form
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'docs': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['user_full_name'].initial = self.instance.user.full_name
            self.fields['user_email'].initial = self.instance.user.email
            self.fields['contact'].initial = self.instance.user.contact

    def save(self, commit=True):
        employee = super(EmployeeForm, self).save(commit=False)
        if commit:
            user = self.instance.user
            user.full_name = self.cleaned_data.get('user_full_name', user.full_name)
            user.email = self.cleaned_data.get('user_email', user.email)
            user.contact = self.cleaned_data.get('contact', user.contact)
            user.save()
            employee.save()
        return employee