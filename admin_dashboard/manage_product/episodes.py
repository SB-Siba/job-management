from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from helpers import utils, api_permission
from django.contrib import messages
from . import forms
import os
from app_common import models as common_model


app = "admin_dashboard/episodes/"


@method_decorator(utils.super_admin_only, name='dispatch')
class EpisodeList(View):
    model = common_model.Episode
    template = app + "episode_list.html"

    def get(self,request):
        episode_list = self.model.objects.all().order_by('id')
        
        paginated_data = utils.paginate(
            request, episode_list, 50
        )
        context = {
            "episode_list":episode_list,
            "data_list":paginated_data
        }
        return render(request, self.template, context)
    
class EpisodeList(View):
    model = common_model.Episode
    template = app + "episode_list.html"

    def get(self,request):
        episode_list = self.model.objects.all().order_by('id')
        
        paginated_data = utils.paginate(
            request, episode_list, 50
        )
        context = {
            "episode_list":episode_list,
            "data_list":paginated_data
        }
        return render(request, self.template, context)
    
@method_decorator(utils.super_admin_only, name='dispatch')
class EpisodeSearch(View):
    model = common_model.Episode
    form_class = forms.CategoryEntryForm
    template = app + "episode_list.html"

    def post(self,request):
        filter_by = request.POST.get("filter_by")
        query = request.POST.get("query")
        product_list = []
        if filter_by == "uid":
            episode_list = self.model.objects.filter(e_id = query)
        else:
            episode_list = self.model.objects.filter(title__icontains = query)

        paginated_data = utils.paginate(
            request, episode_list, 50
        )
        context = {
            "form": self.form_class,
            "episode_list":episode_list,
            "data_list":paginated_data
        }
        return render(request, self.template, context)

class EpisodeSearch(View):
    model = common_model.Episode
    form_class = forms.CategoryEntryForm
    template = app + "episode_list.html"

    def post(self,request):
        filter_by = request.POST.get("filter_by")
        query = request.POST.get("query")
        product_list = []
        if filter_by == "uid":
            episode_list = self.model.objects.filter(e_id = query)
        else:
            episode_list = self.model.objects.filter(title__icontains = query)

        paginated_data = utils.paginate(
            request, episode_list, 50
        )
        context = {
            "form": self.form_class,
            "episode_list":episode_list,
            "data_list":paginated_data
        }
        return render(request, self.template, context)
    
    
@method_decorator(utils.super_admin_only, name='dispatch')
class EpisodeAdd(View):
    model = common_model.Episode
    form_class = forms.EpisodeForm
    template = app + "episode_add.html"

    def get(self,request):
        episode_list = self.model.objects.all().order_by('-id')
        context = {
            "episode_list" : episode_list,
            "form": self.form_class,
        }
        return render(request, self.template, context)
    
    def post(self, request):

        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"Episode is added successfully.....")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return redirect("admin_dashboard:episode_list")
    
@method_decorator(utils.super_admin_only, name='dispatch')
class EpisodeUpdate(View):
    model = common_model.Episode
    form_class = forms.EpisodeForm
    template = app + "episode_update.html"

    def get(self,request, episode_id):
        episode = self.model.objects.get(id = episode_id)
 
        context = {
            "episode" : episode,
            "form": self.form_class(instance=episode),
        }
        return render(request, self.template, context)
    
    def post(self,request, episode_id):

        episode = self.model.objects.get(id = episode_id)
        form = self.form_class(request.POST, request.FILES, instance=episode)

        if form.is_valid():
            form.save()
            messages.success(request, f"Episode ({episode_id}) is updated successfully.....")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return redirect("admin_dashboard:episode_update", episode_id = episode_id)


@method_decorator(utils.super_admin_only, name='dispatch')
class EpisodeDelete(View):
    model = common_model.Episode

    def get(self,request, episode_id):
        print(episode_id,type(episode_id))
        product = self.model.objects.get(id = episode_id)

        product.delete()
        messages.info(request, 'Episode is deleted succesfully......')

        return redirect("admin_dashboard:episode_list")