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


# # =================================================== manage coupon  =============================================

# # class CouponEntryForm(forms.ModelForm):
# #     class Meta:
# #         model = common_models.Coupon
# #         fields = [
# #             'code',
# #             'discount_type',
# #             'discount_digit',
# #             'quantity',
# #             'active',

# #         ]
    
# #     code = forms.CharField(max_length=255)
# #     code.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

# #     discount_type = forms.ChoiceField(choices= common_models.Coupon.DiscountType, initial="flat")
# #     discount_type.widget.attrs.update({'class': 'form-control','type':'text','required':'required'})

# #     discount_digit = forms.IntegerField()
# #     discount_digit.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Amount or Percentage',"required":"required"})

# #     quantity = forms.IntegerField()
# #     quantity.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Coupon Quantity',"required":"required"})

# #     active = forms.ChoiceField(choices= common_models.Coupon.YESNO, initial="yes")
# #     active.widget.attrs.update({'class': 'form-control','type':'text'})

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

    # company = forms.CharField(max_length=255)
    # company.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})


class JobForm(forms.ModelForm):
    class Meta:
        model = common_models.Job
        fields = [
            'title',
            'catagory',
            'description',
            'job_posted_date',
            'show_as_new',

        ]
    
    title = forms.CharField(max_length=255)
    title.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    catagory = forms.ModelChoiceField(queryset = common_models.Catagory.objects.all())
    catagory.widget.attrs.update({'class': 'form-control','type':'text'})

    company_name = forms.CharField(max_length=255)
    company_name.widget.attrs.update({'class': 'form-control','type':'text'})


    description = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","rows":"2"}))
    description.widget.attrs.update({'class': 'form-control','type':'text'})


    job_posted_date = forms.DateField()
    job_posted_date.widget.attrs.update({'class': 'form-control','type':'date',"required":"required"})
    job_posted_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


    # stock = forms.IntegerField(required=True)
    # stock.widget.attrs.update({'class': 'form-control','type':'number'})


    show_as_new = forms.ChoiceField(choices=common_models.Job.YESNO, initial= 'no')
    show_as_new.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})


    # company_image = forms.FileField(
    #     validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg','png']),MaxFileSizeValidator(50*1024)]) # 20 = kb
    # company_image.widget.attrs.update({'class': 'form-control','type':'file'})

    
    
# class JobForm(forms.ModelForm):

#     class Meta:
#         model = common_models.job
#         fields = ['e_id','title','description',]

#     e_id = forms.IntegerField(required=True)
#     e_id.widget.attrs.update({'class': 'form-control','type':'number'})

#     title = forms.CharField(max_length=255)
#     title.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

#     description = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control","rows":"2"}))
#     description.widget.attrs.update({'class': 'form-control','type':'text'})

class EditUserForm(forms.Form):
    email = forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    contact = forms.IntegerField(label="Contact",widget=forms.NumberInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=False)

