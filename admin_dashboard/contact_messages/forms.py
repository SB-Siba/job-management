from django import forms
from app_common import models as common_models

class MessageReply(forms.ModelForm):
    class Meta:
        model = common_models.ContactMessage
        fields = ['status']

    reply = forms.CharField(required=False)
    # reply.widget.attrs.update({'class': 'form-control','type':'text'})

    status = forms.ChoiceField(choices= common_models.ContactMessage.STATUS, initial="read")
    status.widget.attrs.update({'class': 'form-control','type':'text'})