from rest_framework import serializers
from django.conf import settings
from ..serializer import UserSerializer
from app_common import models as common_models

class CartSerializer(serializers.ModelSerializer):
    products_data = serializers.SerializerMethodField()


    def __init__(self, *args, **kwargs):
        self.coupon = kwargs.pop('coupon', None)
        super().__init__(*args, **kwargs)

    #coupon validation and calculation
    # def coupon_validation(self, code, amount):
    #     error_dict = {
    #         "valid" : False,
    #         "discount" : "0",
    #         "message": "Invalid Coupon Code"
    #     }
        
    #     try:
    #         coupon_obj = common_models.Coupon.objects.get(code = code)
    #     except:
    #         return error_dict
        
    #     if coupon_obj.quantity < 1 or coupon_obj.active == 'no':
    #         return error_dict
        
    #     if coupon_obj.discount_type == "flat":
    #         discount = coupon_obj.discount_digit
    #         return {
    #         "coupon":code,
    #         "valid" : True,
    #         "discount" : discount,
    #         "message": f"{code} : is applied successfully"
    #         }
    #     elif coupon_obj.discount_type == "pencentage":
    #         discount = round(amount*(coupon_obj.discount_digit/100),2)
    #         return {
    #             "coupon":code,
    #             "valid" : True,
    #             "discount" : discount,
    #             "message": f"{code} : is applied successfully"
    #         }
    #     else:
    #         return error_dict

    def get_products_data(self,obj):
        total_cart_items = 0
        total_cart_value = 0

        charges = {}

        gross_cart_value = 0 #market price or product_max_price
        our_price = 0
        final_payable_amount =0


        product_list = []

        for key, value in obj.products.items():
            product_total_max__price = value['product']['product_max_price'] * value['quantity']
            gross_cart_value += product_total_max__price

            product_total_discounted__price = value['product']['product_discount_price'] * value['quantity']
            our_price += product_total_discounted__price


            total_cart_items += value['quantity']
            

            value['product']['product_total_price'] = product_total_discounted__price
            
            product_list.append(value)



        discount_amount = gross_cart_value - our_price
        result = {
            'products':product_list,
            'total_cart_items':total_cart_items,
            'gross_cart_value': gross_cart_value,
            'our_price':our_price,
            'discount_amount':discount_amount,
            'discount_percentage': round((discount_amount/gross_cart_value)*100,1),
            'charges':charges,
        }

        # calculating final amount by adding the charges
        final_cart_value = our_price
        if len(charges) > 0:
            for key, value in charges.items():
                final_cart_value += value
        
        #checking is coupon service is on or not
        # result['coupon_enable'] = settings.COUPON_ENABLE

        result['final_cart_value'] = final_cart_value

        #CALCULATE charges -------------------------------------------------

        # GST
        if settings.GST_CHARGE > 0:
            charges['GST']= final_cart_value * settings.GST_CHARGE
            result['final_cart_value'] += charges['GST']
        else:
            charges['GST']=0


        #delivary
        if result['final_cart_value'] < settings.DELIVARY_FREE_ORDER_AMOUNT:
            charges['Delivary']= total_cart_items * settings.DELIVARY_CHARGE_PER_BAG
            result['final_cart_value'] += charges['Delivary']
        else:
            charges['Delivary']= 0


        #modifing coupon data
        if settings.COUPON_ENABLE and self.coupon:
            cuopon_validation_response= self.coupon_validation(self.coupon, final_cart_value)
            result['cuopon_validation_result']=cuopon_validation_response

            if cuopon_validation_response['valid'] == True:
                result['final_cart_value'] -= cuopon_validation_response['discount']
        return result
    

    class Meta:
        model = common_models.Cart
        fields = [
            "products_data",
        ]



class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:

        model = common_models.Order
        fields = '__all__'

