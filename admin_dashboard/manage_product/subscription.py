# from django.shortcuts import render, redirect
# from django.views import View
# from django.utils.decorators import method_decorator
# from helpers import utils, api_permission
# from django.contrib import messages
# from shoppingsite import forms as siteforms
# from admin_dashboard.manage_product import forms
# import os
# from app_common import models as common_model

# app = "admin_dashboard/subscription/"


# @method_decorator(utils.super_admin_only, name='dispatch')
# class SubscriptionPlanList(View):
#     model = common_model.SubscriptionPlan
#     template = app + "subscriptionplan_list.html"

#     def get(self,request):
#         subscriptionplan_obj = self.model.objects.all().order_by('id')

#         paginated_data = utils.paginate(
#             request, subscriptionplan_obj, 50
#         )
#         context = {
#             "subscriptionplan_list":subscriptionplan_obj,
#             "data_list":paginated_data
#         }
#         return render(request, self.template, context)

    
# @method_decorator(utils.super_admin_only, name='dispatch')
# class SubscriptionPlanAdd(View):
#     model = common_model.SubscriptionPlan
#     form_class = siteforms.SubscriptionPlanForm
#     template = app + "subscriptionplan_add.html"

#     def get(self,request):
#         subscriptionplan_list = self.model.objects.all().order_by('-id')
#         context = {
#             "subscriptionplan_list" : subscriptionplan_list,
#             "form": self.form_class,
#         }
#         return render(request, self.template, context)
    
#     def post(self, request):

#         form = self.form_class(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Subscriptionplan is added successfully.....")
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f'{field}: {error}')

#         return redirect("admin_dashboard:subscriptionplan_list")
    
# @method_decorator(utils.super_admin_only, name='dispatch')
# class SubscriptionPlanUpdate(View):
#     model = common_model.SubscriptionPlan
#     form_class = siteforms.SubscriptionPlanForm
#     template = app + "subscriptionplan_update.html"

#     def get(self,request, subscriptionplan_id):
#         subscriptionplan = self.model.objects.get(id = subscriptionplan_id)
 
#         context = {
#             "subscriptionplan" : subscriptionplan,
#             "form": self.form_class(instance=subscriptionplan),
#         }
#         return render(request, self.template, context)
    
#     def post(self,request, subscriptionplan_id):

#         subscriptionplan = self.model.objects.get(id = subscriptionplan_id)
#         form = self.form_class(request.POST, request.FILES, instance=subscriptionplan)

#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Subscription Plan has been updated successfully.....")
#             return redirect("admin_dashboard:subscriptionplan_list")
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f'{field}: {error}')

#         return redirect("admin_dashboard:subscriptionplan_update", subscriptionplan_id = subscriptionplan_id)


# @method_decorator(utils.super_admin_only, name='dispatch')
# class SubscriptionPlanDelete(View):
#     model = common_model.SubscriptionPlan

#     def get(self,request, subscriptionplan_id):
       
#         subscriptionplan = self.model.objects.get(id = subscriptionplan_id)

#         subscriptionplan.delete()
#         messages.info(request, 'Subscription Plan is deleted succesfully......')

#         return redirect("admin_dashboard:subscriptionplan_list")
    




# @method_decorator(utils.super_admin_only, name='dispatch')
# class SubscriptionFeatureList(View):
#     model = common_model.SubscriptionFeatures
#     template = app + "subscriptionfeature_list.html"

#     def get(self,request):
#         subscriptionfeature_obj = self.model.objects.all().order_by('id')
        

#         paginated_data = utils.paginate(
#             request, subscriptionfeature_obj, 50
#         )
#         context = {
#             "subscriptionfeature_list":subscriptionfeature_obj,
#             "data_list":paginated_data
#         }
#         return render(request, self.template, context)
    
# class SubscriptionFeatureList(View):
#     model = common_model.SubscriptionFeatures
#     template = app + "subscriptionfeature_list.html"

#     def get(self,request):
#         subscriptionfeature_obj = self.model.objects.all().order_by('id')

#         paginated_data = utils.paginate(
#             request, subscriptionfeature_obj, 50
#         )
#         context = {
#             "subscriptionfeature_list":subscriptionfeature_obj,
#             "data_list":paginated_data
#         }
#         return render(request, self.template, context)
    
# @method_decorator(utils.super_admin_only, name='dispatch')
# class SubscriptionFeatureAdd(View):
#     model = common_model.SubscriptionFeatures
#     form_class = siteforms.SubscriptionFeaturesForm
#     template = app + "subscriptionfeature_add.html"

#     def get(self,request):
#         subscriptionfeature_list = self.model.objects.all().order_by('-id')
#         context = {
#             "subscriptionfeature_list" : subscriptionfeature_list,
#             "form": self.form_class,
#         }
#         return render(request, self.template, context)
    
#     def post(self, request):

#         form = self.form_class(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Subscription Feature is added successfully.....")
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f'{field}: {error}')

#         return redirect("admin_dashboard:subscriptionfeature_list")
    
# @method_decorator(utils.super_admin_only, name='dispatch')
# class SubscriptionFeatureSearch(View):
#     model = common_model.SubscriptionFeatures
#     form_class = forms.CategoryEntryForm
#     template = app + "subscriptionfeature_list.html"

#     def post(self,request):
#         filter_by = request.POST.get("filter_by")
#         query = request.POST.get("query")
#         product_list = []
#         if filter_by == "uid":
#             subscriptionfeature_list = self.model.objects.filter(id = query)
#         else:
#             subscriptionfeature_list = self.model.objects.filter(feature__icontains = query)

#         paginated_data = utils.paginate(
#             request, subscriptionfeature_list, 50
#         )
#         context = {
#             "form": self.form_class,
#             "subscriptionfeature_list":subscriptionfeature_list,
#             "data_list":paginated_data
#         }
#         return render(request, self.template, context)
    
# class SubscriptionFeatureSearch(View):
#     model = common_model.SubscriptionFeatures
#     form_class = forms.CategoryEntryForm
#     template = app + "subscriptionfeature_list.html"

#     def post(self,request):
#         filter_by = request.POST.get("filter_by")
#         query = request.POST.get("query")
#         product_list = []
#         if filter_by == "uid":
#             subscriptionfeature_list = self.model.objects.filter(id = query)
#         else:
#             subscriptionfeature_list = self.model.objects.filter(feature__icontains = query)

#         paginated_data = utils.paginate(
#             request, subscriptionfeature_list, 50
#         )
#         context = {
#             "form": self.form_class,
#             "subscriptionfeature_list":subscriptionfeature_list,
#             "data_list":paginated_data
#         }
#         return render(request, self.template, context)
    
# @method_decorator(utils.super_admin_only, name='dispatch')
# class SubscriptionFeatureUpdate(View):
#     model = common_model.SubscriptionFeatures
#     form_class = siteforms.SubscriptionFeaturesForm
#     template = app + "subscriptionfeature_update.html"

#     def get(self,request, subscriptionfeature_id):
#         subscriptionfeature = self.model.objects.get(id = subscriptionfeature_id)
 
#         context = {
#             "subscriptionfeature" : subscriptionfeature,
#             "form": self.form_class(instance=subscriptionfeature),
#         }
#         return render(request, self.template, context)
    
#     def post(self,request, subscriptionfeature_id):

#         subscriptionfeature = self.model.objects.get(id = subscriptionfeature_id)
#         form = self.form_class(request.POST, request.FILES, instance=subscriptionfeature)

#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Subscription Plan has been updated successfully.....")
#             return redirect("admin_dashboard:subscriptionfeature_list")
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f'{field}: {error}')

#         return redirect("admin_dashboard:subscriptionfeature_update", subscriptionfeature_id = subscriptionfeature_id)


# @method_decorator(utils.super_admin_only, name='dispatch')
# class SubscriptionFeatureDelete(View):
#     model = common_model.SubscriptionFeatures

#     def get(self,request, subscriptionfeature_id):
       
#         subscriptionfeature = self.model.objects.get(id = subscriptionfeature_id)

#         subscriptionfeature.delete()
#         messages.info(request, 'Subscription Feature is deleted succesfully......')

#         return redirect("admin_dashboard:subscriptionfeature_list")
    
# @method_decorator(utils.super_admin_only, name='dispatch')
# class SubscriptionUserList(View):
#     model = common_model.UserSubscription
#     template = app + "subscribe_users.html"
#     def get(self,request):
#         subscription_user = self.model.objects.all()

#         return render(request,self.template,locals())