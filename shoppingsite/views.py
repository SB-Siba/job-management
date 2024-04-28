from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.views import View
from django.contrib import messages
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from . import forms
from . import rozerpay
from app_common.checkout.serializer import CartSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from io import StringIO
import json
from app_common.models import (
    AudioBook,
    Category,
    Cart,
    UserProfile,
    User,
    Episode,
    SubscriptionFeatures,
    SubscriptionPlan,
    UserSubscription,
    Order,
)

from helpers.utils import dict_filter  # Import dict_filter function
import json

app = "shoppingsite/"


class HomeView(View):
    template = app + "home.html"

    def get(self, request):
        category_obj = Category.objects.all()
        audioBooks = AudioBook.objects.all().order_by("-id")[:10]
        return render(request, self.template, locals())


class ProfileView(View):
    template = app + "userprofile.html"

    def get(self, request):
        user = request.user
        print(user)
        category_obj = Category.objects.all()
        userobj = User.objects.get(email=user.email)
        try:
            profileobj = UserProfile.objects.get(user=userobj)
        except UserProfile.DoesNotExist:
            profileobj = None

        if not user.is_authenticated:
            return redirect("shoppingsite:login")

        return render(request, self.template, locals())


class UpdateProfileView(View):
    template = app + "update_profile.html"
    form = forms.UpdateProfileForm

    def get(self, request):
        user = request.user
        category_obj = Category.objects.all()
        userobj = User.objects.get(email=user.email)

        try:
            profileObj = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profileObj = None
        except:
            pass

        initial_data = {
            "email": userobj.email,
            "full_name": userobj.full_name,
            "contact": userobj.contact,
            "bio": profileObj.bio,
            "profile_pic": profileObj.profile_pic,
        }
        form = self.form(initial=initial_data)

        return render(request, self.template, locals())

    def post(self, request):
        category_obj = Category.objects.all()
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            full_name = form.cleaned_data["full_name"]
            contact = form.cleaned_data["contact"]
            bio = form.cleaned_data["bio"]
            profile_picture = form.cleaned_data["profile_pic"]
            password = form.cleaned_data["password"]

            user = request.user

            try:
                userobj = User.objects.get(email=user.email)
                userobj.email = email
                userobj.full_name = full_name
                userobj.contact = contact

                profile_object = UserProfile.objects.filter(user=user)

                if profile_picture is None:
                    picture = ""
                    for i in profile_object:
                        picture = i.profile_pic
                else:
                    picture = profile_picture

                if len(profile_object) == 0:
                    profileobj = UserProfile(user=user, bio=bio, profile_pic=picture)
                    profileobj.save()
                else:
                    for i in profile_object:
                        i.user = user
                        i.profile_pic = picture
                        i.bio = bio
                        i.save()

                if len(password) > 0:
                    userobj.set_password(password)
                    messages.success(request, "Password Changed Successfully")

                userobj.save()
                return redirect("shoppingsite:profile")

            except:
                messages.error(request, "Error in Updating Profile")
        return render(request, self.template, locals())


class AllAddress(View):
    template = app + "alladdress.html"

    def get(self, request):
        user = request.user
        addresses = user.address or []  # This will return a list of addresses

        return render(request, self.template, {"addresses": addresses})


from uuid import uuid4


class AddAddress(View):
    template = app + "addaddress.html"
    form = forms.AddressForm

    def get(self, request):
        form = self.form()
        return render(request, self.template, locals())

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            landmark1 = form.cleaned_data["landmark1"]
            landmark2 = form.cleaned_data["landmark2"]
            country = form.cleaned_data["country"]
            state = form.cleaned_data["state"]
            city = form.cleaned_data["city"]
            zipcode = form.cleaned_data["zipcode"]

            address_id = str(uuid4())

            address_data = {
                "id": address_id,
                "landmark1": landmark1,
                "landmark2": landmark2,
                "country": country,
                "state": state,
                "city": city,
                "zipcode": zipcode,
            }

            user = request.user
            addresses = user.address or []

            # Append the new address data to the list of addresses
            addresses.append(address_data)

            # Save the updated list of addresses back to the user model
            user.address = addresses
            user.save()

            return redirect("shoppingsite:alladdress")
        else:
            return redirect("shoppingsite:addaddress")


class DeleteAddress(View):
    def get(self, request, address_id):
        user = request.user
        addresses = user.address or []

        # Filter out the address with the specified ID
        addresses = [
            address for address in addresses if address.get("id") != address_id
        ]

        # Update the user model with the modified list of addresses
        user.address = addresses
        user.save()

        return redirect("shoppingsite:alladdress")


class showProductsViews(View):
    template = app + "productsofcategory.html"

    def get(self, request, c_name):
        user = request.user
        subscription_user = UserSubscription.objects.filter(user=user)
        s_user_length = subscription_user.count()
        category_obj = Category.objects.all()
        products_for_this_category = AudioBook.objects.filter(category__title=c_name)
        return render(request, self.template, locals())


class ProductDetailsView(View):
    model = AudioBook
    template = app + "product_details.html"

    def get(self, request, p_id):
        user = request.user
        cart_obj = Cart.objects.filter(products__id=p_id)
        category_obj = Category.objects.all()
        product_obj = self.model.objects.get(id=p_id)
        episodes = Episode.objects.filter(audiobook=product_obj).order_by("e_id")
        subscription_user = UserSubscription.objects.filter(user__id=user.id)
        s_user_length = subscription_user.count()

        return render(request, self.template, locals())


class ShowCart(View):
    def get(self, request):
        category_obj = Category.objects.all()
        user = request.user
        if not user.is_authenticated:
            context = {"cartItems": []}
        else:
            try:
                cartItems = Cart.objects.get(user=user)
                totaloriginalprice = 0
                totalPrice = 0
                GST = 0
                Delivary = 0
                final_cart_value = 0
                products = {}
                obj = CartSerializer(cartItems).data
                print(obj)
                for i,j in obj.items():
                    totaloriginalprice = int(j['gross_cart_value'])
                    totalPrice = int(j['our_price'])
                    GST = j['charges']['GST']
                    Delivary = j['charges']['Delivary']
                    final_cart_value = j['final_cart_value']
                
                for key, value in cartItems.products.items():
                    prd_obj = AudioBook.objects.get(title=str(key))
                    products[prd_obj] = value
                discount_price = totaloriginalprice - totalPrice
                # taxprice = totalPrice*(3/100)
                # aftertaxprice = totalPrice+taxprice

                cartItems.total_price = totalPrice
                cartItems.save()

            except Exception as e:
                print('Error :', str(e))
                products = {}

        return render(request, "shoppingsite/cartpage.html", locals())


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        product_obj = AudioBook.objects.get(id=product_id)
        product_name = ""
        cart, created = Cart.objects.get_or_create(user=request.user)

        products = cart.products or {}
        products[str(product_obj.title)] = (
            products.get(str(product_obj.title), 0) + quantity
        )
        cart.products = products

        total_price = sum(
            AudioBook.objects.get(title=name).book_discount_price * qty
            for name, qty in products.items()
        )
        cart.total_price = total_price

        cart.save()

        return redirect("shoppingsite:showcart")

    def get(self, request, *args, **kwargs):
        return redirect("home")


def RemoveFromCart(request, cart_id, rp_name):
    cart = get_object_or_404(Cart, id=cart_id)
    if str(rp_name) in cart.products:
        if cart.products[str(rp_name)] > 1:
            cart.products[str(rp_name)] -= 1
            cart.save()
        else:
            del cart.products[str(rp_name)]
            cart.save()

    return redirect("shoppingsite:showcart")


class PricingPageView(View):
    template = app + "pricingpage.html"

    def get(self, request):
        category_obj = Category.objects.all()
        subcription_plans = SubscriptionPlan.objects.all()
        features = {}
        for i in subcription_plans:
            subscription_feature = SubscriptionFeatures.objects.filter(sub_plan=i)
            features[i] = list(subscription_feature)
        return render(request, self.template, locals())


class SubscriptionAudioBooks(View):
    model = AudioBook
    template = app + "subscription_products.html"

    def get(self, request):
        category_obj = Category.objects.all()
        user = request.user
        subsc_user_obj = UserSubscription.objects.filter(user=user)
        if subsc_user_obj is not None:
            product_obj = AudioBook.objects.all()

        return render(request, self.template, locals())


class SubscribeBooksEpisode(View):
    template = app + "episodesofsubscribebook.html"

    def get(self, request, book_id):
        userId = request.user.id
        category_obj = Category.objects.all()
        book_obj = AudioBook.objects.get(id=book_id)
        episodes = Episode.objects.filter(audiobook__in=[book_obj])

        return render(request, self.template, locals())


def UserTakeSubscription(request, plan_id):
    user = request.user
    plan_obj = SubscriptionPlan.objects.get(id=plan_id)
    try:
        subs_qset = UserSubscription.objects.filter(user=user, plan=plan_obj).count()
        if subs_qset > 0:
            messages.error(request, "This user already has a subscription to this plan")
            return redirect("shoppingsite:pricing")
        else:
            new_subscription = UserSubscription(user=user, plan=plan_obj)
            new_subscription.save()
            messages.success(
                request, "You have successfully subscribed for the selected Plan!"
            )
            return redirect("shoppingsite:home")
    except:
        messages.error(request, "Error while Taking Subscription")
        return redirect("shoppingsite:pricing")


class Checkout(View):
    template = app + "checkout.html"
    model = Order

    def get(self, request):
        user = request.user
        cart = Cart.objects.get(user=user)
        total_price = cart.total_price
        user = request.user
        addresses = user.address or []
        print(addresses)
        # status, rz_order_id = rozerpay.create_order_in_razPay(
        #     amount=int(cart.total_price)
        # )
        # print("over",rz_order_id)

        context = {
            "cart": cart.products,
            # "rz_order_id": rz_order_id,
            "amount": cart.total_price,
            # "api_key": settings.RAZORPAY_API_KEY,
            "total_price":total_price,
            "addresses":addresses
        }

        return render(request, self.template, context)

@method_decorator(csrf_exempt, name='dispatch')
class PaymentSuccess(View):

    model = Order

    def post(self, request):
        user = request.user
        cart = Cart.objects.get(user=request.user)
        data = json.loads(request.body)
        address_id = data.get('address_id')
        order_details = CartSerializer(cart).data
        ord_meta_data = {}
        print(ord_meta_data)
        for i,j in order_details.items():
            ord_meta_data.update(j)
        print(ord_meta_data)
        user_addresses = user.address
        selected_address = None
        for address in user_addresses:
            if address['id'] == address_id:
                selected_address = address
                break
        # razorpay_payment_id = request.POST['razorpay_payment_id']
        # razorpay_order_id = request.POST['razorpay_order_id']
        # razorpay_signature = request.POST['razorpay_signature']

        # if rozerpay.verify_signature(request.POST):
        # print("order_placed")
        try:
            order = self.model(
                user=user,
                full_name=cart.user.full_name,
                email=cart.user.email,
                products=cart.products,
                order_value=cart.total_price,
                address=selected_address,
                order_meta_data = ord_meta_data
                # razorpay_payment_id = razorpay_payment_id,
                # razorpay_order_id= razorpay_order_id,
                # razorpay_signature= razorpay_signature,
            )
            # order.order_meta_data = json.loads(ord_meta_data)
            order.save()
            messages.success(request, "Order Successful!")
            cart.delete()
            return redirect("shoppingsite:home")
        except Exception as e:
            print(e)
            messages.error(request, "Error while placing Order.")
            return redirect("shoppingsite:checkout")
        # else:
        #     print('payment is not varified')

# class PaymentHandler(View):
#     model = Cart

#     def get(self, request):

#         cart = self.model.objects.get(user=request.user)
#         print("jhabhja k")
#         status, rz_order_id = rozerpay.create_order_in_razPay(
#             amount=int(cart.total_price)
#         )
#         print("over",rz_order_id)

#         context = {
#             "cart": cart.products,
#             "rz_order_id": rz_order_id,
#             "amount": cart.total_price,
#             "api_key": settings.RAZORPAY_API_KEY,
#         }
#         return JsonResponse(context, safe=False)


class DirectBuy(View):
    template = app + "checkout.html"

    def get(self, request, p_id):
        user = request.user
        product_obj = AudioBook.objects.get(id=p_id)
        total_price = product_obj.book_discount_price
        return render(request, self.template, locals())

    def post(self, request, p_id):
        user = request.user
        product_obj = AudioBook.objects.get(id=p_id)
        user_obj = User.objects.get(id=user.id)

        fullName = request.POST["fullName"]
        email = request.POST["email"]
        # Address
        address = request.POST["address"]
        address2 = request.POST["address2"]
        city = request.POST["city"]
        state = request.POST["state"]
        zipcode = request.POST["zip"]
        country = request.POST["country"]
        phone = request.POST["phone"]
        # card values
        paymentMethod = request.POST["paymentMethod"]
        cc_name = request.POST["cc-name"]
        cc_number = request.POST["cc-number"]
        cc_expiration = request.POST["cc-expiration"]
        cc_cvv = request.POST["cc-cvv"]

        order_address = {
            "main_address": address,
            "sub_address": address2,
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "country": country,
            "phone": phone,
        }

        product_dict = {product_obj.title: 1}

        try:
            order = Order(
                user=request.user,
                products=product_dict,
                order_value=product_obj.book_discount_price,
                payment_type=paymentMethod,
                address=order_address,
            )
            order.save()
            messages.success(request, "Order Successful!")
            return redirect("shoppingsite:home")
        except Exception:
            messages.error(request, "Error while placing Order.")
            return redirect("shoppingsite:productdetails", p_id)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def remove_audio(request):
    if request.method == "POST":
        audio_path = request.POST.get("audioPath")
        # Perform validation on audio_path if needed
        # Remove the audio file
        import os

        print(audio_path)
        try:
            audio_obj = Episode.objects.filter(audio_file=audio_path)
            print(audio_obj)
            if os.path.exists(audio_path):
                print("before")
                os.remove(audio_path)
                print("after")
                messages.success(
                    request, {"message": "Audio file removed successfully"}
                )
            else:
                messages.error(request, {"error": "Audio file not found"})
        except Exception as e:
            messages.error(request, {"error": str(e)})
    else:
        messages.error(request, {"error": "Method not allowed"})
