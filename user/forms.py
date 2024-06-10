from django import forms
from django.contrib.auth.forms import PasswordChangeForm,UserCreationForm
from app_common import models as common_models

class SignUpForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    contact = forms.IntegerField(max_value=10 ,help_text='Required. Enter a valid contact number .',
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    Resume=forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password',widget=forms.PasswordInput(attrs= {'autofocus':True,'autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label='New Password',widget=forms.PasswordInput(attrs= {'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Cofirm Password',widget=forms.PasswordInput(attrs= {'autocomplete':'current-password','class':'form-control'}))


# class StudentForm(forms.Form):  
#     firstname = forms.CharField(label="Enter first name",max_length=50)  
#     lastname  = forms.CharField(label="Enter last name", max_length = 10)  
#     email     = forms.EmailField(label="Enter Email")  
#     resume      = forms.FileField() # for creating file input


class UpdateProfileForm(forms.Form):
    
    email = forms.EmailField(max_length=255)
    email.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Email',"required":"required"})

    full_name = forms.CharField(max_length=255)
    full_name.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Full Name',"required":"required"})

    contact = forms.IntegerField()
    contact.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Mobile Number',"required":"required"})

    skills = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control","rows":"1"}))
    skills.widget.attrs.update({'class': 'form-control','type':'text'})

    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs= {'autocomplete':'current-password','class':'form-control','placeholder':'Only if you want to change then type here.'}),required=False)

    profile_pic = forms.FileField(label='Select an image file', required=False)
    profile_pic.widget.attrs.update({'class': 'form-control', 'type': 'file'})

    resume = forms.FileField(label='Select an pdf file', required=False)
    resume.widget.attrs.update({'class': 'form-control', 'type': 'file'})
    
# class AddressForm(forms.Form):
#     landmark1 = forms.CharField(max_length=255)
#     landmark1.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

#     landmark2 = forms.CharField(max_length=255)
#     landmark2.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})
    
#     country = forms.CharField(max_length=255)
#     country.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

#     state = forms.CharField(max_length=255)
#     state.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

#     city = forms.CharField(max_length=255)
#     city.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})
    
#     zipcode = forms.IntegerField()
#     zipcode.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Pincode',"required":"required"})

# class SubscriptionPlanForm(forms.ModelForm):

#     class Meta:
#         model = common_models.SubscriptionPlan
#         fields = ['title','price','days']

#     title = forms.CharField(max_length=255)
#     title.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

#     price = forms.IntegerField()
#     price.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Price',"required":"required"})

#     days = forms.IntegerField()
#     days.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Days',"required":"required"})

# class SubscriptionFeaturesForm(forms.ModelForm):
#     class Meta:
#         model = common_models.SubscriptionFeatures
#         fields = ['sub_plan','feature']

#     sub_plan = forms.ModelChoiceField(queryset = common_models.SubscriptionPlan.objects.all())
#     sub_plan.widget.attrs.update({'class': 'form-control','type':'text'})

#     feature = forms.CharField(max_length=255)
#     feature.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

# class OrderForm(forms.Form):
#     full_name = forms.CharField(max_length=255)
#     full_name.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Full Name',"required":"required"})

#     phone_no = forms.IntegerField()
#     phone_no.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Mobile Number',"required":"required"})

#     email = forms.EmailField(max_length=255)
#     email.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Email',"required":"required"})

#     address = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control","rows":"1"}))
#     address.widget.attrs.update({'class': 'form-control','type':'text'})

#     address2 = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control","rows":"1"}))
#     address2.widget.attrs.update({'class': 'form-control','type':'text'})

#     country = forms.CharField(max_length=255)
#     country.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

#     state = forms.CharField(max_length=255)
#     state.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

#     city = forms.CharField(max_length=255)
#     city.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})
    
#     zipcode = forms.IntegerField()
#     zipcode.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Pincode',"required":"required"})


class ContactMessageForm(forms.Form):

    user = forms.CharField(max_length=255)
    user.widget.attrs.update({'class': 'form-control','type':'text',"required":"required","readonly":"readonly"})

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter Your Message'
        }),
        required=True
    )


# class PartnerForm(forms.ModelForm):
#     class Meta:
#         model = common_models.BecomeAPartner
#         fields = ['name', 'email', 'phone_number', 'company_name', 'website', 'industry', 'number_of_employees', 'partnership_interest', 'partnership_type', 'past_experience', 'additional_information']
#         widgets = {
#             'partnership_interest': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
#             'past_experience': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
#             'additional_information': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
#             'company_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'website': forms.URLInput(attrs={'class': 'form-control'}),
#             'industry': forms.TextInput(attrs={'class': 'form-control'}),
#             'number_of_employees': forms.NumberInput(attrs={'class': 'form-control'}),
#             'partnership_type': forms.TextInput(attrs={'class': 'form-control'}),
#         }

#