# quotation/forms.py
from app_common.models import Job, User
from django import forms
from .models import Invoice, Quotation, Quotation2
from django.forms import modelformset_factory, formset_factory
from django.core.validators import RegexValidator
# from .models import Invoice, Job

class QuotationForm(forms.ModelForm):
    EXPERIENCE_CHOICES = [
        ('FRESHER', 'FRESHER (Min. 1yr experience)'),
        ('EXPERIENCED', 'Experienced (Min. 5 yrs)')
    ]
    client = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active = True),
        required=False,
        widget=forms.Select(attrs={'placeholder': 'Choose Client'})
    )

    job_title = forms.ModelChoiceField(
        queryset=Job.objects.all(),
        required=False,
        widget=forms.Select(attrs={'placeholder': 'Select job title'})
    )
    
    number_of_persons = forms.IntegerField(
        min_value=1, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Enter number of persons'})
    )
    experience_level = forms.ChoiceField(
        choices=EXPERIENCE_CHOICES, required=True, widget=forms.Select(attrs={'placeholder': 'Select experience level'})
    )
    salary = forms.DecimalField(
        max_digits=10, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Enter salary'})
    )

    class Meta:
        model = Quotation
        fields = ['client','job_title', 'number_of_persons', 'experience_level', 'salary']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['client'].queryset = User.objects.filter(is_staff=True, is_superuser=False)
        
        self.fields['client'].widget.attrs.update({'placeholder': 'Choose Client'})
        self.fields['job_title'].widget.attrs.update({'placeholder': 'Select job title'})
        self.fields['number_of_persons'].widget.attrs.update({'placeholder': 'Enter number of persons'})
        self.fields['experience_level'].widget.attrs.update({'placeholder': 'Select experience level'})
        self.fields['salary'].widget.attrs.update({'placeholder': 'Enter salary'})

class QuotationForm2(forms.ModelForm):

    company_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter Company Name"
        })
    )

    subject = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Subject'
        })
    )

    to = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Recipient'
        })
    )

    notification_text = forms.CharField(
        initial="AS PER LABOUR & ESI DEPARTMENT NOTIFICATION DT. 13.03.2024, GoO",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Notification Text',
        })
    )

    vendor_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter Vendor's Name"
        })
    )

    post1 = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter Post Name"
        })
    )
    
    post2 = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter Post Name"
        })
    )

    # Semi-skilled
    semi_skilled = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Semi Skilled Rate'
        })
    )
    
    semi_skilled_manpower = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control manpower-field',
        })
    )

    # Unskilled
    unskilled = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Unskilled Rate'
        })
    )

    unskilled_manpower = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control manpower-field',
        })
    )

    # Skilled
    skilled = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Skilled Rate'
        })
    )
    
    skilled_manpower = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control manpower-field',
        })
    )

    # High-skilled
    high_skilled = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter High Skilled Rate'
        })
    )

    high_skilled_manpower = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control manpower-field',
        })
    )

    # Working hours and days
    working_hours = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Working Hours',
        })
    )

    working_days = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Working Days',
        })
    )

    # Other Allowances
    other_allowances_semi_skilled = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Other Allowances for Semi Skilled'
        })
    )

    other_allowances_unskilled = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Other Allowances for Unskilled'
        })
    )

    other_allowances_skilled = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Other Allowances for Skilled'
        })
    )

    other_allowances_high_skilled = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Other Allowances for High Skilled'
        })
    )

    # Uniform Cost
    semi_uniform_cost = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Uniform Cost for Semi skilled'
        })
    )

    un_uniform_cost = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Uniform Cost for Unskilled'
        })
    )

    skilled_uniform_cost = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Uniform Cost for Skilled'
        })
    )

    high_skilled_uniform_cost = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Uniform Cost for High Skilled'
        })
    )

    # Reliever Cost
    semi_reliever_cost = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Reliever Cost for Semi skilled'
        })
    )

    un_reliever_cost = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Reliever Cost for Unskilled'
        })
    )

    skilled_reliever_cost = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Reliever Cost for Skilled'
        })
    )

    high_skilled_reliever_cost = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Reliever Cost for High Skilled'
        })
    )

    # Operational Cost
    semi_operational_cost = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Operational Cost for Semi skilled'
        })
    )

    un_operational_cost = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Operational Cost for Unskilled'
        })
    )

    skilled_operational_cost = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Operational Cost for Skilled'
        })
    )

    high_skilled_operational_cost = forms.DecimalField(
        max_digits=6, decimal_places=2, 
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Operational Cost for High Skilled'
        })
    )

    class Meta:
        model = Quotation2
        fields = [
            'company_name', 'subject', 'to', 'vendor_name', 'notification_text', 'semi_skilled', 'semi_skilled_manpower', 
            'unskilled', 'unskilled_manpower', 'skilled', 'skilled_manpower', 'high_skilled', 'high_skilled_manpower',
            'working_hours', 'working_days', 'other_allowances_semi_skilled', 'other_allowances_unskilled', 'other_allowances_skilled', 'other_allowances_high_skilled',
            'semi_uniform_cost', 'un_uniform_cost', 'skilled_uniform_cost', 'high_skilled_uniform_cost',
            'semi_reliever_cost', 'un_reliever_cost', 'skilled_reliever_cost', 'high_skilled_reliever_cost',
            'semi_operational_cost', 'un_operational_cost', 'skilled_operational_cost', 'high_skilled_operational_cost', 
            'post1', 'post2'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and not user.is_superuser:
            for field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True

class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'company_name',
            'address',
            'description', 
            'esi',
            'epf',
        ]

        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'Company Name'}),
            'address': forms.Textarea(attrs={'placeholder': 'Address'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'}),
            'esi': forms.NumberInput(attrs={'placeholder': 'Enter ESI Amount', 'step': '0.01'}),
            'epf': forms.NumberInput(attrs={'placeholder': 'Enter EPF Amount', 'step': '0.01'}),
        }

class EmployeeDetailsForm(forms.Form):
    employee_name = forms.CharField(max_length=100, initial='Unknown Employee', widget=forms.TextInput(attrs={'placeholder': 'Employee Name'}))
    days_of_duty = forms.DecimalField(max_digits=5, decimal_places=1, initial=0, widget=forms.NumberInput(attrs={'placeholder': 'Days of Duty'}))
    overtime_days = forms.FloatField(initial=0, widget=forms.NumberInput(attrs={'placeholder': 'Overtime Days'}))
    total_work_days = forms.FloatField(initial=0, widget=forms.NumberInput(attrs={'placeholder': 'Total Work Days'}))
    price_per_day = forms.FloatField(initial=0, widget=forms.NumberInput(attrs={'placeholder': 'Price Per Day'}))
    total_price = forms.FloatField(initial=0, widget=forms.NumberInput(attrs={'placeholder': 'Total Price'}))
    remark = forms.CharField(max_length=250, required=False, widget=forms.Textarea(attrs={'placeholder': 'Remarks'}))