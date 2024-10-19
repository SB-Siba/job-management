from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from helpers import utils
from django.urls import reverse_lazy

# Importing necessary modules for API and forms
from . import forms
from app_common import models as common_model

app = "admin_dashboard/manage_product/"

# ================================================== sector management ==========================================

@method_decorator(utils.super_admin_only, name='dispatch')
class SectorList(View):
    model = common_model.Sector
    form_class = forms.sectorEntryForm
    template = app + "sector_list.html"

    def get(self, request):
        # Get all sectors and order by id
        sector_list = self.model.objects.all().order_by('-id')
        sectors = []
        product_count = []
        
        # Get the count of jobs for each sector
        for sector in sector_list:
            p_obj = common_model.Job.objects.filter(sector=sector).count()
            sectors.append(sector)
            product_count.append(p_obj)
        
        # Zip sectors and job counts together for rendering in template
        sector_product_count_zip = zip(sectors, product_count)
        context = {
            "form": self.form_class,
            "sector_product_count_zip": sector_product_count_zip,
        }
        return render(request, self.template, context)
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"{request.POST['title']} is added to the list.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
        
        return redirect("admin_dashboard:sector_list")

@method_decorator(utils.super_admin_only, name='dispatch')
class SectorAdd(View):
    model = common_model.Sector
    form_class = forms.sectorEntryForm
    template = app + "sector_add.html"

    def get(self, request):
        sector_list = self.model.objects.all().order_by('-id')
        context = {
            "sector_list": sector_list,
            "form": self.form_class,
        }
        return render(request, self.template, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Sector added successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
        
        return redirect("admin_dashboard:sector_list")

@method_decorator(utils.super_admin_only, name='dispatch')
class SectorUpdate(View):
    model = common_model.Sector
    form_class = forms.sectorEntryForm
    template = app + "sector_update.html"

    def get(self, request, sector_id):
        sector = self.model.objects.get(id=sector_id)
        context = {
            "form": self.form_class(instance=sector),
        }
        return render(request, self.template, context)

    def post(self, request, sector_id):
        sector = self.model.objects.get(id=sector_id)
        form = self.form_class(request.POST, request.FILES, instance=sector)
        if form.is_valid():
            form.save()
            messages.success(request, f"{request.POST['title']} is updated successfully.")
            return redirect("admin_dashboard:sector_list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return render(request, self.template, {'form': form})


class SectorDeleteView(View):
    model = common_model.Sector
    success_url = reverse_lazy('admin_dashboard:sector_list')

    def post(self, request, *args, **kwargs):
        sector_id = kwargs.get('pk')
        sector = get_object_or_404(self.model, id=sector_id)
        sector.delete()
        messages.info(request, 'Sector deleted successfully.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return JsonResponse({'success': False}, status=400)
