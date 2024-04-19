from django import forms
from app_common import models as common_models

class MessageReply(forms.ModelForm):
    class Meta:
        model = common_models.ContactMessage
        fields = ['reply','status']

    reply = forms.CharField(required=False,widget=forms.Textarea(attrs={"class":"form-control","rows":"2","required":"required","placeholder":"Leave a reply here"}))
    reply.widget.attrs.update({'class': 'form-control','type':'text'})

    status = forms.ChoiceField(choices= common_models.ContactMessage.STATUS, initial="read")
    status.widget.attrs.update({'class': 'form-control','type':'text',})