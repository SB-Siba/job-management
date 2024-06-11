from django.shortcuts import render, redirect

import json
from helpers import utils, api_permission
from django.forms.models import model_to_dict

# for api
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
# -------------------------------------------- custom import
from .. import swagger_doc

from app_common import models as common_model
from . import serializer as cart_serializer
# from .. import tasks

# class CartList(APIView):    

#     permission_classes = [api_permission.is_authenticated]
#     serializer_class= cart_serializer.CartSerializer
#     model= common_model.Products

#     @swagger_auto_schema(
#         tags=["cart"],
#         operation_description="Cart-item list",
#     )

#     def get(self, request):
#         try:
#             cart = common_model.Cart.objects.get(user = request.user)
#         except Exception as e:
#             return Response({
#                 'status':400,
#                 "error":['Empty Cart Found....',],
#             })


#         try:
#             product_list = self.serializer_class(cart, coupon = cart.coupon).data
#         except Exception as e:
#             print(e)
#             product_list = []
#         return Response({
#             "status":200,
#             "product_list": product_list
            
#         })




# class ApiAddTOCart(APIView):

#     permission_classes = [api_permission.is_authenticated]
#     serializer_class= cart_serializer.CartSerializer
#     model= common_model.Products

#     @swagger_auto_schema(
#         tags=["cart"],
#         operation_description="Add to Cart",
#     )
#     def post(self, request, product_uid):
        
#         cart, created = common_model.Cart.objects.get_or_create(user = request.user)

#         product=  self.model.objects.get(uid = product_uid)
#         product_dict = model_to_dict(product)

#         product_dict.pop('image')
#         product_dict['image'] = product.image.url or None

#         if product.uid not in cart.products:
#             cart.products[product.uid] = {
#                 "product": product_dict,
#                 "quantity": 1
#             }
#         else:
#             cart.products[product.uid]['quantity'] += 1
        
#         cart.save()

#         return Response({
#             "status":200,
#             "message": f"{product.name[:10]}... is added to cart.",
            
#         })
    


# class ApiCartUpdateDelete(APIView):

#     permission_classes = [api_permission.is_authenticated]
#     serializer_class= cart_serializer.CartSerializer
#     model= common_model.Products

#     @swagger_auto_schema(
#         tags=["cart"],
#         operation_description="Update Product Quantity",
#         manual_parameters=swagger_doc.update_cart,
#     )   

#     def put(self, request, product_uid):
#         quantity = request.data.get('quantity', None)

#         cart = common_model.Cart.objects.get(user = request.user)
        
#         if product_uid not in cart.products:
#             return Response({
#                 "status":400,
#                 "message": f"Product is not present in cart..",
#             })
#         else:
#             if quantity:
#                 cart.products[product_uid]['quantity'] = int(quantity)
        
#         cart.save()


#         cart = self.serializer_class(cart, coupon = cart.coupon).data


#         return Response({
#             "status":200,
#             "message": "Your Cart is updated",
#             "product_list": cart,
                                                                                                                                                                                                                                                                                                                                                                                                                         
#         })
    
#     @swagger_auto_schema(
#         tags=["cart"],
#         operation_description="Remove Product from cart",
#     )  

#     def delete(self, request, product_uid):
#         cart, created = common_model.Cart.objects.get_or_create(user = request.user)

#         if product_uid not in cart.products:
#             return Response({
#                 "status":400,
#                 "message": f"Product is not present in cart..",
#             })
#         else:
#             cart.products.pop(product_uid)
        
#         cart.save()

#         try:
#             product_list = self.serializer_class(cart).data
#         except Exception as e:
#             print(e)
#             product_list = []

#         return Response({
#             "status":200,
#             "message": "Item removed from Cart",
#             "product_list": product_list,
            
#         })
    

# class ApplyCoupon(APIView):

#     permission_classes = [api_permission.is_authenticated]
#     serializer_class= cart_serializer.CartSerializer
#     model= common_model.Products

#     @swagger_auto_schema(
#         tags=["cart"],
#         operation_description="Apply Coupon",
#     )   

#     def get(self, request, coupon_code):

#         cart = common_model.Cart.objects.get(user = request.user)
#         cart.coupon = coupon_code
#         cart.save()

#         cart = self.serializer_class(cart, coupon = cart.coupon).data

#         return Response({
#             "status":200,
#             "message": "Your Cart is updated",
#             "product_list": cart,
                                                                                                                                                                                                                                                                                                                                                                                                                         
#         })

#     @swagger_auto_schema(
#         tags=["cart"],
#         operation_description="remove Coupon",
#     ) 
#     def delete(self, request, coupon_code):

#         cart = common_model.Cart.objects.get(user = request.user)
#         cart.coupon = None
#         cart.save()

#         cart = self.serializer_class(cart, coupon = cart.coupon ).data

#         return Response({
#             "status":200,
#             "message": "Coupon is Removed",
#             "product_list": cart,
                                                                                                                                                                                                                                                                                                                                                                                                                         
#         })
    

# class PlaceOrder(APIView):
#     permission_classes = [api_permission.is_authenticated]
#     model = common_model.Order
#     cart_serializer = cart_serializer.CartSerializer


#     @swagger_auto_schema(
#         tags=["Order"],
#         operation_description="Place Order",
#         manual_parameters=swagger_doc.order_placed,
#     )
#     def update_product(self,product_dict=[]):
#         for product_obj in product_dict:
#             product = common_model.Products.objects.get(uid = product_obj['product']['uid'])
#             product.stock -= product_obj['quantity']
#             product.save()

#     def build_address(self, address={}):
#         print(address)

#     def get(self, request):
#         address = request.GET.get('address_title')
#         payment_status = request.GET.get("payment_status")
#         payment_method = request.GET.get("payment_method")
#         transaction_id = request.GET.get("transaction_id", None)

#         # ====================== getting cart items ====================
#         try:
#             cart = common_model.Cart.objects.get(user = request.user)
#         except Exception as e:
#             return Response({
#                 "status" : 400,
#                 "error" : "Your Cart is Empty..."
#             })
        
#         #======================== get cart serialized data along with all calculation ===============
         

#         cart_serializer_data = self.cart_serializer(cart, coupon = cart.coupon).data

#         # ========================== creating an order object =========================
#         if len(cart_serializer_data) > 0:

#             order_obj = self.model.objects.create(
#                 user = request.user,
#                 coupon = cart.coupon,
#                 payment_status=payment_status,
#                 payment_method=payment_method,
#                 transaction_id=transaction_id,
#                 products = cart_serializer_data["products_data"]["products"],
#                 order_value = cart_serializer_data["products_data"]["final_cart_value"],
#                 address = request.user.address[address],
#             )

#             # ====================== making meta data by deleting some data ==================================
            
#             product_list =cart_serializer_data["products_data"]['products']

#             cart_serializer_data["products_data"].pop('products', None)
#             cart_serializer_data["products_data"].pop('final_cart_value', None)

#             order_obj.order_meta_data = cart_serializer_data["products_data"]
#             order_obj.save()

        
#         # ========================= delete cart object =======================
#         #cart.delete()

#         # ========================= coupon update ============================
#         if cart.coupon:
#             try:
#                 coupon_obj = common_model.Coupon.objects.get(code = cart.coupon)
#                 coupon_obj.quantity -= 1
#                 coupon_obj.save()
#             except:
#                 pass
                
        
#         # --------------------- product stock update --------------
#         self.update_product(product_list)

#         #---------------------  send invoice ----------------
#         tasks.share_invoice.delay(
#             request.user.email,
#             cart_serializer.OrderSerializer(order_obj).data,
#         )
        

#         return Response({
#             "status":200,
#             "order":cart_serializer.OrderSerializer(order_obj).data,
#         })


class OrderList(APIView):
    permission_classes = [api_permission.is_authenticated]
    model = common_model.Order
    serializer = cart_serializer.OrderSerializer
    pagination_class = utils.CustomPagination(50)


    @swagger_auto_schema(
        tags=["Order"],
        operation_description="Order List",
    )  
    def get(self, request):
        order_list = self.model.objects.filter(user = request.user).order_by("-id")

        paginator = self.pagination_class
        page = paginator.paginate_queryset(order_list, request)
        serialized_data= self.serializer(page, many=True).data

        return Response({
            'status': 200,
            'order_list': serialized_data,
            'pagination_meta_data': paginator.pagination_meta_data(),

        })


class OrderDetail(APIView):
    permission_classes = [api_permission.is_authenticated]
    model = common_model.Order
    serializer_class = cart_serializer.OrderSerializer

    @swagger_auto_schema(
        tags=["Order"],
        operation_description="Order Detail API",
    )  
    def get(self, request, uid):
        order = self.model.objects.get(user = request.user, uid = uid)

        return Response({
            'status': 200,
            'order_list': self.serializer_class(order).data,

        })


# class OrderCancelReturnRefund(APIView):
#     permission_classes = [api_permission.is_authenticated]
#     model = common_model.Order
#     serializer = cart_serializer.OrderSerializer
#     manual_parameters=swagger_doc.order_cancel_return_refund,

#     @swagger_auto_schema(
#         tags=["Order"],
#         operation_description="Order Cancel / Refund / Return",
#         manual_parameters=swagger_doc.order_cancel_return_refund,
#     )  
#     def post(self, request, order_uid):
#         order_status = request.data.get("order_status")
#         more_info = request.data.get("more_info")

#         order = self.model.objects.get(user = request.user, uid = order_uid)

#         if order.order_status == "Accepted" or order.order_status == "On-Way":
#             return Response({
#                 "status":400,
#                 "error": f"Order is {order.order_status} cancle/refund/return is not possible.",
#             })
#         else:
#             order.order_status = order_status
#             order.more_info = more_info
#             order.save()

#         return Response({
#             'status': 200,
#             "message": "Your request is recived..."
#         })