# quotation/forms.py
from app_common.models import Job, User
from django import forms
from .models import Quotation, QuotationItem, Invoice
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

class CreateInvoiceForm(forms.ModelForm):
    notification_text = forms.CharField(
        initial="AS PER LABOUR & ESI DEPARTMENT NOTIFICATION DT. 13.03.2024, GoO",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Notification Text',
        })
    )

    company_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter Vendor's Name"
        })
    )

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

    class Meta:
        model = Invoice
        fields = [
            'company_name', 'notification_text', 'semi_skilled', 'semi_skilled_manpower', 
            'unskilled', 'unskilled_manpower', 'working_hours', 'working_days', 
            'other_allowances_semi_skilled', 'other_allowances_unskilled', 'semi_uniform_cost', 'un_uniform_cost',
            'semi_reliever_cost', 'un_reliever_cost', 'semi_operational_cost', 'un_operational_cost'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and not user.is_superuser:
            for field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True

