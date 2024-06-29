from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from client.models import Client
from admin.forms import ClientForm 


def is_admin(user):
    return user.is_staff

@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminClientListView(View):
    def get(self, request):
        clients = Client.objects.all()
        return render(request, 'admin/client_list.html', {'clients': clients})

@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminClientCreateView(View):
    def get(self, request):
        form = ClientForm()
        return render(request, 'admin/client_form.html', {'form': form})
    
    def post(self, request):
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_client_list')
        return render(request, 'admin/client_form.html', {'form': form})
