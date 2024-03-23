# from django.shortcuts import render, redirect
# from django.views import View
# from django.contrib import messages
# from django.utils.decorators import method_decorator
# from helpers import utils, api_permission
# from django.forms.models import model_to_dict

# from helpers import utils
# from app_common import models as common_model
# from app_common.checkout.serializer import OrderSerializer
# from .forms import OrderUpdateForm
# from ..tasks import update_order_status

# app = "admin_dashboard/order/"

# # ================================================== patient management ==========================================

# @method_decorator(utils.super_admin_only, name='dispatch')
# class OrderList(View):
#     model = common_model.Order
#     template = app + "order_list.html"

#     def get(self,request):

#         order_list = self.model.objects.all().order_by('-id')
#         paginated_data = utils.paginate(request, order_list, 50)
#         order_status_options = common_model.Order.ORDER_STATUS
        
#         context = {
#             "order_list":paginated_data,
#             "order_status_options":order_status_options,
#         }
#         return render(request, self.template,context)

# @method_decorator(utils.super_admin_only, name='dispatch')
# class OrderStatusSearch(View):
#     model = common_model.Order
#     template = app + "order_list.html"

#     def get(self,request):
#         filter_by = request.GET.get('filter_by')
#         order_list = self.model.objects.filter(order_status = filter_by)
#         paginated_data = utils.paginate(request, order_list, 50)
#         order_status_options = common_model.Order.ORDER_STATUS
        
#         context = {
#             "order_list":paginated_data,
#             "order_status_options":order_status_options,
#         }
#         return render(request, self.template,context)


# @method_decorator(utils.super_admin_only, name='dispatch')
# class OrderSearch(View):
#     model = common_model.Order
#     template = app + "order_list.html"

#     def get(self,request):
#         query = request.GET.get('query')
#         order_list = self.model.objects.filter(uid__icontains = query)
#         context = {
#             "order_list":order_list,
#         }
#         return render(request, self.template,context)


# @method_decorator(utils.super_admin_only, name='dispatch')
# class OrderDetail(View):
#     model = common_model.Order
#     form_class = OrderUpdateForm
#     template= app + "order_detail.html"

#     def get(self,request, order_uid):
#         order = self.model.objects.get(uid = order_uid)
        
#         product_list = []
#         total_quantity= 0
        

#         for product in order.products:
#             product['product']['quantity'] = product['quantity']
#             total_quantity += product['quantity']
#             product_list.append(product['product'])

#         context={
#             'order':order,
#             'product_list':product_list,
#             'total_quantity':total_quantity,
#             'address':order.address,
#             'form':OrderUpdateForm(instance = order)
#         }
#         return render(request, self.template, context)
    
#     def post(self,request, order_uid):
#         order = self.model.objects.get(uid = order_uid)

#         form = self.form_class(request.POST, instance = order)

#         if form.is_valid():
#             obj=form.save()
#             update_order_status.delay(obj.user.email, OrderSerializer(obj).data)
#             messages.success(request, 'Order Status is updated....')

#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f'{field}: {error}')

#         return redirect('admin_dashboard:order_detail', order_uid = order_uid)


# @method_decorator(utils.super_admin_only, name='dispatch')
# class DownloadInvoice(View):
#     model = common_model.Order
#     form_class = OrderUpdateForm
#     template= 'app_common/checkout/invoice.html'

#     def get(self,request, order_uid):
#         order = self.model.objects.get(uid = order_uid)
#         data = OrderSerializer(order).data
#         for product in data['products']:
#             product['product']['quantity']=product['quantity']

#         context ={
#             'order':data,
#             'address':data['address'],
#             'user':order.user,
#             'product_list':data['products'],
#             'charges':data['order_meta_data']['charges'],
#             'gross_amt':data['order_meta_data']['our_price'],
#             'discount':data['order_meta_data']['our_price'] - data['order_value'],
#         }

#         return render(request, self.template, context)
        