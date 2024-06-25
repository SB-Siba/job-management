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
# from app_common.contact.serializer import ContactMessageSerializer
from .forms import MessageReply

app = "admin_dashboard/contact_messages/"

# ================================================== product management ==========================================


@method_decorator(utils.super_admin_only, name='dispatch')
class AdminInbox(View):
    template_name = 'admin_app/inbox.html'
    model = common_model.ContactMessage()
    def get(self, request):
        received_messages = model.objects.filter(status='pending').order_by('-created_at')
        paginated_messages = paginate(request, received_messages, 50)
        return render(request, self.template_name, {'received_messages': paginated_messages})

@method_decorator(utils.super_admin_only, name='dispatch')
class AdminMessageDetail(View):
    template_name = 'admin_app/message_detail.html'
    model = common_model.ContactMessage()
    def get(self, request, uid):
        message = get_object_or_404(model, uid=uid)
        if message.status == 'pending':
            message.status = 'read'
            message.save()
        form = MessageReply(instance=message)
        return render(request, self.template_name, {'message': message, 'form': form})

@method_decorator(utils.super_admin_only, name='dispatch')
class AdminMessageReply(View):
    form_class = MessageReply
    model = common_model.ContactMessage()
    def post(self, request, uid):
        message = get_object_or_404(model, uid=uid)
        form = self.form_class(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'}, status=200)
        else:
            error_list = [f'{field}: {error}' for field, errors in form.errors.items() for error in errors]
            return JsonResponse({'errors': error_list}, status=400)