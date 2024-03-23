# from django.shortcuts import render, redirect
# from django.views import View
# from django.contrib import messages
# from django.utils.decorators import method_decorator
# from django.conf import settings
# from helpers import utils, api_permission

# from . import forms
# from app_common import models as common_model


# app = "admin_dashboard/manage_product/"

# # ================================================== patient management ==========================================

# @method_decorator(utils.super_admin_only, name='dispatch')
# class CouponList(View):
#     model = common_model.Coupon
#     form_class = forms.CouponEntryForm
#     template = app + "coupon_list.html"

#     def get(self,request):
#         coupon_list = self.model.objects.all().order_by('-id')
#         context = {
#             "form": self.form_class,
#             "coupon_list":coupon_list,
#         }
#         return render(request, self.template, context)
    
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"{request.POST['code']} is added to list.....")
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f'{field}: {error}')

#         return redirect("admin_dashboard:coupon_list")


# @method_decorator(utils.super_admin_only, name='dispatch')
# class CuponUpdate(View):
#     model = common_model.Coupon
#     form_class = forms.CouponEntryForm
#     template = app + "coupon_update.html"

#     def get(self,request, coupon_id):
#         coupon = self.model.objects.get(id= coupon_id)
#         context = {
#             "form": self.form_class(instance=coupon),
#         }
#         return render(request, self.template, context)
    
#     def post(self, request, coupon_id):
#         coupon = self.model.objects.get(id= coupon_id)
#         form = self.form_class(request.POST, instance= coupon)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Coupon is updated successfully.....")
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f'{field}: {error}')

#         return redirect("admin_dashboard:coupon_update", coupon_id = coupon_id)


# @method_decorator(utils.super_admin_only, name='dispatch')
# class CouponDelete(View):
#     model = common_model.Coupon

#     def get(self,request, coupon_id):
#         coupon = self.model.objects.get(id= coupon_id).delete()
#         messages.info(request, "Coupon is deleted successfully....")
#         return redirect("admin_dashboard:coupon_list")
