from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from app_common import models as common_models

class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password',widget=forms.PasswordInput(attrs= {'autofocus':True,'autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label='New Password',widget=forms.PasswordInput(attrs= {'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Cofirm Password',widget=forms.PasswordInput(attrs= {'autocomplete':'current-password','class':'form-control'}))


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

