from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from app_common import models as common_models

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

    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control","rows":"1"}))
    bio.widget.attrs.update({'class': 'form-control','type':'text'})

    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs= {'autocomplete':'current-password','class':'form-control','placeholder':'Only if you want to change then type here.'}),required=False)

    profile_pic = forms.FileField(label='Select an audio file')
    profile_pic.widget.attrs.update({'class': 'form-control','type':'file'})
    
class AddressForm(forms.Form):
    landmark1 = forms.CharField(max_length=255)
    landmark1.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    landmark2 = forms.CharField(max_length=255)
    landmark2.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})
    
    country = forms.CharField(max_length=255)
    country.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    state = forms.CharField(max_length=255)
    state.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    city = forms.CharField(max_length=255)
    city.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})
    
    zipcode = forms.IntegerField()
    zipcode.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Pincode',"required":"required"})

class SubscriptionPlanForm(forms.ModelForm):

    class Meta:
        model = common_models.SubscriptionPlan
        fields = ['title','price','days']

    title = forms.CharField(max_length=255)
    title.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    price = forms.IntegerField()
    price.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Price',"required":"required"})

    days = forms.IntegerField()
    days.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Days',"required":"required"})

class SubscriptionFeaturesForm(forms.ModelForm):
    class Meta:
        model = common_models.SubscriptionFeatures
        fields = ['sub_plan','feature']

    sub_plan = forms.ModelChoiceField(queryset = common_models.SubscriptionPlan.objects.all())
    sub_plan.widget.attrs.update({'class': 'form-control','type':'text'})

    feature = forms.CharField(max_length=255)
    feature.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

class OrderForm(forms.Form):
    full_name = forms.CharField(max_length=255)
    full_name.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Full Name',"required":"required"})

    phone_no = forms.IntegerField()
    phone_no.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Mobile Number',"required":"required"})

    email = forms.EmailField(max_length=255)
    email.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Email',"required":"required"})

    address = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control","rows":"1"}))
    address.widget.attrs.update({'class': 'form-control','type':'text'})

    address2 = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control","rows":"1"}))
    address2.widget.attrs.update({'class': 'form-control','type':'text'})

    country = forms.CharField(max_length=255)
    country.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    state = forms.CharField(max_length=255)
    state.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    city = forms.CharField(max_length=255)
    city.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})
    
    zipcode = forms.IntegerField()
    zipcode.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Pincode',"required":"required"})