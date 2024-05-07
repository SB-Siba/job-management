from rest_framework import serializers
from django.conf import settings
from ..serializer import UserSerializer
from app_common import models as common_models
from django.shortcuts import get_object_or_404
from decimal import Decimal

class CartSerializer(serializers.ModelSerializer):
    products_data = serializers.SerializerMethodField()


    def __init__(self, *args, user_has_subscription=False, **kwargs):
        self.user_has_subscription = user_has_subscription
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


        products = {}
        product_list = []

        for key,value in obj.products.items():
            product = get_object_or_404(common_models.AudioBook,title = key)
            gross_cart_value += product.book_max_price*int(value)

            if self.user_has_subscription:
                print("hbhij")
                product_total_discounted__price = float(product.book_discount_price_for_members)*int(value)
                our_price += product_total_discounted__price
                price = product.book_discount_price_for_members
            else:
                print("false")
                product_total_discounted__price = float(product.book_discount_price)*int(value)
                our_price += product_total_discounted__price
                price = product.book_discount_price

            # product_total_discounted_price = price * int(value)
            # our_price += product_total_discounted_price

            total_cart_items += int(value)

            x = {}
            x['quantity'] = value
            x['price_per_unit'] = price
            x['total_price'] = float(price) * int(value)

            products[key] = x
        print(gross_cart_value,our_price)
        discount_amount = gross_cart_value - our_price
        result = {
            'products':products,
            'total_cart_items':total_cart_items,
            'gross_cart_value': gross_cart_value,
            'our_price':our_price,
            'discount_amount':discount_amount,
            'discount_percentage': round((discount_amount/gross_cart_value)*100,1),
            'charges':charges,
        }

        # calculating final amount by adding the charges
        final_cart_value = Decimal(str(our_price))
        if len(charges) > 0:
            for key, value in charges.items():
                final_cart_value += value
        
        #checking is coupon service is on or not
        # result['coupon_enable'] = settings.COUPON_ENABLE

        result['final_cart_value'] = final_cart_value

        #CALCULATE charges -------------------------------------------------

        # GST
        if settings.GST_CHARGE > 0:
            gst_value = final_cart_value * Decimal(str(settings.GST_CHARGE))
            charges['GST'] = '{:.2f}'.format(gst_value)
        else:
            charges['GST']=0
        
        #delivary
        if result['final_cart_value'] < settings.DELIVARY_FREE_ORDER_AMOUNT:
            delevery_charge = total_cart_items * Decimal(str(settings.DELIVARY_CHARGE_PER_BAG))
            charges['Delivary'] = '{:.2f}'.format(delevery_charge)
        else:
            charges['Delivary']= 0

        for key, value in charges.items():
            final_cart_value += Decimal(value)

        #modifing coupon data
        if settings.COUPON_ENABLE and self.coupon:
            cuopon_validation_response= self.coupon_validation(self.coupon, final_cart_value)
            result['cuopon_validation_result']=cuopon_validation_response

            if cuopon_validation_response['valid'] == True:
                result['final_cart_value'] -= cuopon_validation_response['discount']

        result['final_cart_value'] = float(final_cart_value)

        return result
    

    class Meta:
        model = common_models.Cart
        fields = [
            "products_data",
        ]


# ____________________
class DirectBuySerializer(serializers.ModelSerializer):
    products_data = serializers.SerializerMethodField()


    def __init__(self, *args, user_has_subscription=False, **kwargs):
        self.user_has_subscription = user_has_subscription
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
        total_items = 1
        total_value = 0
        charges = {}
        gross_value = 0 #market price or product_max_price
        our_price = 0
        final_payable_amount =0


        products = {}
        product_list = []

        try:
            product = get_object_or_404(common_models.AudioBook,uid = obj.uid)
            gross_value += float(product.book_max_price)
            #____________
            product_discounted__price = float(product.book_discount_price)
            our_price = product_discounted__price
            price = product.book_discount_price

            x = {}
            
            x['quantity'] = 1
            x['price_per_unit'] = price
            x['total_price'] = float(price)

            products[product.title] = x
            #______________

            
        except Exception as e:
            print(e)
        discount_amount = gross_value - our_price
        result = {
            'products':products,
            'total_items':total_items,
            'gross_value': gross_value,
            'our_price':our_price,
            'discount_amount':discount_amount,
            'discount_percentage': round((discount_amount/gross_value)*100,1),
            'charges':charges,
        }

        # calculating final amount by adding the charges
        final_value = Decimal(str(our_price))
        if len(charges) > 0:
            for key, value in charges.items():
                final_value += value
        
        #checking is coupon service is on or not
        # result['coupon_enable'] = settings.COUPON_ENABLE

        result['final_value'] = final_value

        #CALCULATE charges -------------------------------------------------

        # GST
        if settings.GST_CHARGE > 0:
            gst_value = final_value * Decimal(str(settings.GST_CHARGE))
            charges['GST'] = '{:.2f}'.format(gst_value)
        else:
            charges['GST']=0
        
        #delivary
        if result['final_value'] < settings.DELIVARY_FREE_ORDER_AMOUNT:
            delevery_charge = total_items * Decimal(str(settings.DELIVARY_CHARGE_PER_BAG))
            charges['Delivary'] = '{:.2f}'.format(delevery_charge)
        else:
            charges['Delivary']= 0

        for key, value in charges.items():
            final_value += Decimal(value)

        #modifing coupon data
        if settings.COUPON_ENABLE and self.coupon:
            cuopon_validation_response= self.coupon_validation(self.coupon, final_value)
            result['cuopon_validation_result']=cuopon_validation_response

            if cuopon_validation_response['valid'] == True:
                result['final_value'] -= cuopon_validation_response['discount']

        result['final_value'] = float(final_value)

        return result
    

    class Meta:
        model = common_models.AudioBook
        fields = [
            "products_data",
        ]

#==============================Subscription Serializer
class TakeSubscriptionSerializer(serializers.ModelSerializer):
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
        total_items = 1
        total_value = 0
        charges = {}
        gross_value = 0 #market price or product_max_price
        our_price = 0
        final_payable_amount =0


        products = {}
        product_list = []

        try:
            plan = get_object_or_404(common_models.SubscriptionPlan,id = obj.id)
            gross_value += float(plan.price)

            product_discounted__price = float(plan.price)
            our_price = product_discounted__price

            x = {}
            
            x['quantity'] = 1
            x['price_per_unit'] = float(plan.price)
            x['total_price'] = float(plan.price)

            products[plan.title] = x
        except Exception as e:
            print(e)
        discount_amount = gross_value - our_price
        result = {
            'products':products,
            'total_items':total_items,
            'gross_value': gross_value,
            'our_price':our_price,
            'discount_amount':discount_amount,
            'discount_percentage': round((discount_amount/gross_value)*100,1),
            'charges':charges,
        }

        # calculating final amount by adding the charges
        final_value = Decimal(str(our_price))
        if len(charges) > 0:
            for key, value in charges.items():
                final_value += value
        
        #checking is coupon service is on or not
        # result['coupon_enable'] = settings.COUPON_ENABLE

        result['final_value'] = final_value

        #CALCULATE charges -------------------------------------------------

        # GST
        if settings.GST_CHARGE > 0:
            gst_value = final_value * Decimal(str(settings.GST_CHARGE))
            charges['GST'] = '{:.2f}'.format(gst_value)
        else:
            charges['GST']=0
        
        #delivary
        if result['final_value'] < settings.DELIVARY_FREE_ORDER_AMOUNT:
            delevery_charge = total_items * Decimal(str(settings.DELIVARY_CHARGE_PER_BAG))
            charges['Delivary'] = '{:.2f}'.format(delevery_charge)
        else:
            charges['Delivary']= 0

        for key, value in charges.items():
            final_value += Decimal(value)

        #modifing coupon data
        if settings.COUPON_ENABLE and self.coupon:
            cuopon_validation_response= self.coupon_validation(self.coupon, final_value)
            result['cuopon_validation_result']=cuopon_validation_response

            if cuopon_validation_response['valid'] == True:
                result['final_value'] -= cuopon_validation_response['discount']

        result['final_value'] = float(final_value)

        return result
    

    class Meta:
        model = common_models.SubscriptionPlan
        fields = [
            "products_data",
        ]


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:

        model = common_models.Order
        fields = '__all__'

