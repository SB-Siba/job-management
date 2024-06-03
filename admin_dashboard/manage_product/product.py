# from django.shortcuts import render, redirect
# from django.views import View
# from django.contrib import messages
# from django.utils.decorators import method_decorator
# from django.conf import settings
# #import requests
# from django.http import JsonResponse
# import json
# from helpers import utils, api_permission
# from django.forms.models import model_to_dict
# import os

# # for api
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from drf_yasg.utils import swagger_auto_schema
# # -------------------------------------------- custom import
# from .. import swagger_doc
# from . import serializer as product_serializer
# from . import forms
# from app_common import models as common_model


# app = "admin_dashboard/manage_product/"

# # ================================================== product management ==========================================

# @method_decorator(utils.super_admin_only, name='dispatch')
# class AudioBookList(View):
#     model = common_model.AudioBook
#     template = app + "product_list.html"

#     def get(self,request):
#         product_list = self.model.objects.all().order_by('-id')
        
#         paginated_data = utils.paginate(
#             request, product_list, 50
#         )
#         context = {
#             "product_list":product_list,
#             "data_list":paginated_data
#         }
#         return render(request, self.template, context)
    


# class AudioBookList(View):
#     model = common_model.AudioBook
#     template = app + "product_list.html"

#     def get(self,request):
#         product_list = self.model.objects.all().order_by('-id')
        
#         paginated_data = utils.paginate(
#             request, product_list, 50
#         )
#         context = {
#             "product_list":product_list,
#             "data_list":paginated_data
#         }
#         return render(request, self.template, context)


# @method_decorator(utils.super_admin_only, name='dispatch')
# class AudioBookSearch(View):
#     model = common_model.AudioBook
#     form_class = forms.CategoryEntryForm
#     template = app + "product_list.html"

#     def post(self,request):
#         filter_by = request.POST.get("filter_by")
#         query = request.POST.get("query")
#         product_list = []
#         if filter_by == "uid":
#             product_list = self.model.objects.filter(id = query)
#         else:
#             product_list = self.model.objects.filter(title__icontains = query)

#         paginated_data = utils.paginate(
#             request, product_list, 50
#         )
#         context = {
#             "form": self.form_class,
#             "product_list":product_list,
#             "data_list":paginated_data
#         }
#         return render(request, self.template, context)



# class AudioBookSearch(View):
#     model = common_model.AudioBook
#     form_class = forms.CategoryEntryForm
#     template = app + "product_list.html"

#     def post(self,request):
#         filter_by = request.POST.get("filter_by")
#         query = request.POST.get("query")
#         product_list = []
#         if filter_by == "uid":
#             product_list = self.model.objects.filter(id = query)
#         else:
#             product_list = self.model.objects.filter(title__icontains = query)

#         paginated_data = utils.paginate(
#             request, product_list, 50
#         )
#         context = {
#             "form": self.form_class,
#             "product_list":product_list,
#             "data_list":paginated_data
#         }
#         return render(request, self.template, context)

# @method_decorator(utils.super_admin_only, name='dispatch')
# class AudioBookFilter(View):
#     model = common_model.AudioBook
#     template = app + "product_list.html"

#     def get(self,request):
#         filter_by = request.GET.get("filter_by")

#         if filter_by == "trending":
#             product_list = self.model.objects.filter(trending="yes").order_by('-id')

#         elif filter_by == "show_as_new":
#             product_list = self.model.objects.filter(show_as_new="yes").order_by('-id')

#         elif filter_by == "display_as_bestseller":
#             product_list = self.model.objects.filter(display_as_bestseller="yes").order_by('-id')

#         elif filter_by == "hide":
#             product_list = self.model.objects.filter(hide="yes").order_by('-id')        

#         else:
#             product_list = self.model.objects.filter().order_by('-id')

#         paginated_data = utils.paginate(
#             request, product_list, 50
#         )

#         context = {
#             "product_list":product_list,
#             "data_list":paginated_data
#         }
#         return render(request, self.template, context)
    

# class AudioBookFilter(View):
#     model = common_model.AudioBook
#     template = app + "product_list.html"

#     def get(self,request):
#         filter_by = request.GET.get("filter_by")

#         if filter_by == "trending":
#             product_list = self.model.objects.filter(trending="yes").order_by('-id')

#         elif filter_by == "show_as_new":
#             product_list = self.model.objects.filter(show_as_new="yes").order_by('-id')

#         elif filter_by == "display_as_bestseller":
#             product_list = self.model.objects.filter(display_as_bestseller="yes").order_by('-id')

#         elif filter_by == "hide":
#             product_list = self.model.objects.filter(hide="yes").order_by('-id')        

#         else:
#             product_list = self.model.objects.filter().order_by('-id')

#         paginated_data = utils.paginate(
#             request, product_list, 50
#         )

#         context = {
#             "product_list":product_list,
#             "data_list":paginated_data
#         }
#         return render(request, self.template, context)
    

# @method_decorator(utils.super_admin_only, name='dispatch')
# class APIProductFilter(View):
#     model = common_model.AudioBook
#     template = app + "product_list.html"

#     def get(self,request):
#         filter_by = request.GET.get("filter_by", None)

#         if filter_by == "trending":
#             product_list = self.model.objects.filter(trending="yes").order_by('-id')

#         elif filter_by == "show_as_new":
#             product_list = self.model.objects.filter(show_as_new="yes").order_by('-id')

#         elif filter_by == "display_as_bestseller":
#             product_list = self.model.objects.filter(display_as_bestseller="yes").order_by('-id')

#         elif filter_by == "hide":
#             product_list = self.model.objects.filter(hide="yes").order_by('-id')        

#         else:
#             product_list = self.model.objects.filter().order_by('-id')

#         paginated_data = utils.paginate(
#             request, product_list, 50
#         )
        
#         context = {
#             "product_list":product_list,
#             "data_list":paginated_data
#         }
#         return render(request, self.template, context)



# class CatagoryProductFilter(APIView):
#     permission_classes = [api_permission.is_authenticated]
#     serializer_class= product_serializer.ProductSerializer
#     model= common_model.AudioBook
#     pagination_class = utils.CustomPagination(50)


#     @swagger_auto_schema(
#         tags=["product"],
#         operation_description="Product List as per catagory...",
#     )
#     def get(self,request, catagory_id ):
        
#         product_list = self.model.objects.filter(category__id = catagory_id).order_by('-id')

#         paginator = self.pagination_class
#         page = paginator.paginate_queryset(product_list, request)
#         serialized_data= self.serializer_class(page, many=True).data

#         return Response({
#             'status': 200,
#             'product_list': serialized_data,
#             'pagination_meta_data': paginator.pagination_meta_data(),

#         })


# class ApiProductList(APIView):

#     permission_classes = [api_permission.is_authenticated]
#     serializer_class= product_serializer.ProductSerializer
#     model= common_model.AudioBook
#     pagination_class = utils.CustomPagination(50)

#     @swagger_auto_schema(
#         tags=["product"],
#         operation_description="It will return product list. Available filters: ['hide','all']",
#         manual_parameters=swagger_doc.product_filter,
#     )
#     def get(self, request):

#         filter_by = request.GET.get("filter_by", None)

#         if filter_by == "trending":
#             product_list = self.model.objects.filter(trending="yes").order_by('-id')

#         elif filter_by == "show_as_new":
#             product_list = self.model.objects.filter(show_as_new="yes").order_by('-id')

#         elif filter_by == "display_as_bestseller":
#             product_list = self.model.objects.filter(display_as_bestseller="yes").order_by('-id')

#         elif filter_by == "hide":
#             product_list = self.model.objects.filter(hide="yes").order_by('-id')        

#         else:
#             product_list = self.model.objects.filter().order_by('-id')

#         paginator = self.pagination_class
#         page = paginator.paginate_queryset(product_list, request)
#         serialized_data= self.serializer_class(page, many=True).data

#         return Response({
#             'status': 200,
#             'product_list': serialized_data,
#             'pagination_meta_data': paginator.pagination_meta_data(),

#         })


# class ApiProductDetail(APIView):

#     permission_classes = [api_permission.is_authenticated]
#     serializer_class= product_serializer.ProductSerializer
#     model= common_model.AudioBook

#     @swagger_auto_schema(
#         tags=["product"],
#         operation_description="Product Detail API",
#     )
#     def get(self, request, product_uid):

#         product = self.model.objects.get(id = product_uid)
#         serialized_data= self.serializer_class(product).data

#         return Response({
#             'status': 200,
#             'product': serialized_data,

#         })

# @method_decorator(utils.super_admin_only, name='dispatch')
# class AudioBookAdd(View):
#     model = common_model.AudioBook
#     form_class = forms.AudioBookForm
#     template = app + "product_add.html"

#     def get(self,request):
#         product_list = self.model.objects.all().order_by('-id')
#         context = {
#             "product_list" : product_list,
#             "form": self.form_class,
#         }
#         return render(request, self.template, context)
    
#     def post(self, request):

#         form = self.form_class(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Product is added successfully.....")
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f'{field}: {error}')

#         return redirect("admin_dashboard:product_list")


# @method_decorator(utils.super_admin_only, name='dispatch')
# class AudioBookUpdate(View):
#     model = common_model.AudioBook
#     form_class = forms.AudioBookForm
#     template = app + "product_update.html"

#     def get(self,request, product_uid):
#         product = self.model.objects.get(id = product_uid)
 
#         context = {
#             "product" : product,
#             "form": self.form_class(instance=product),
#         }
#         return render(request, self.template, context)
    
#     def post(self,request, product_uid):

#         product = self.model.objects.get(id = product_uid)
#         form = self.form_class(request.POST, request.FILES, instance=product)

#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Product ({product_uid}) is updated successfully.....")
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f'{field}: {error}')

#         return redirect("admin_dashboard:product_update", product_uid = product_uid)


# @method_decorator(utils.super_admin_only, name='dispatch')
# class AudioBookDelete(View):
#     model = common_model.AudioBook

#     def get(self,request, product_uid):
#         product = self.model.objects.get(id = product_uid)

#         if product.image:
#             image_path = product.image.path
#             os.remove(image_path)

#         product.delete()
#         messages.info(request, 'Product is deleted succesfully......')

#         return redirect("admin_dashboard:product_list")