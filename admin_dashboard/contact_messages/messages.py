from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator

#import requests
from django.http import JsonResponse
import json

# -------------------------------------------- custom import
from helpers import utils
from app_common import models as common_model
from app_common.contact.serializer import ContactMessageSerializer
from .forms import MessageReply

app = "admin_dashboard/contact_messages/"

# ================================================== product management ==========================================

@method_decorator(utils.super_admin_only, name='dispatch')
class ContactMessageList(View):
    model = common_model.ContactMessage
    form_class = MessageReply
    template = app + "message_list.html"

    def get(self,request):
        message_list = self.model.objects.all().order_by('-id')
        paginated_data = utils.paginate(request, message_list, 50)

        context = {
            "message_list": paginated_data,
            "form": self.form_class,
        }
        return render(request, self.template, context)
    

@method_decorator(utils.super_admin_only, name='dispatch')
class ContactMessageDetail(View):
    model = common_model.ContactMessage


    def get(self,request, uid):
        message = self.model.objects.get(uid = uid)
        return JsonResponse(ContactMessageSerializer(message).data, safe=False)


@method_decorator(utils.super_admin_only, name='dispatch')
class ContactMessagereply(View):
    model = common_model.ContactMessage
    form_class = MessageReply

    def post(self,request, uid):

        message = self.model.objects.get(uid = uid)
        form = self.form_class(json.loads(request.body), instance= message)
        if form.is_valid():
            form.save()
            return JsonResponse(200, safe=False)
        else:
            error_list = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_list.append(f'{field}: {error}')
            print(error_list)
            return JsonResponse(error_list, safe=False)