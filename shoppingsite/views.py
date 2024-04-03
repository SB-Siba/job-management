from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from django.views import View
from django.contrib import messages
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from . import forms
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
    Order
)

from helpers.utils import dict_filter  # Import dict_filter function
import json

app = "shoppingsite/"


class HomeView(View):
    template = app + "home.html"
    def get(self,request):
        category_obj = Category.objects.all()
        return render(request,self.template,locals())
    
class ProfileView(View):
    template = app + "userprofile.html"
    def get(self, request):
        user=request.user
        print(user)
        category_obj = Category.objects.all()
        userobj = User.objects.get(email=user.email)
        try:
            profileobj = UserProfile.objects.get(user=userobj)
        except UserProfile.DoesNotExist:
            profileobj = None
            
        if not user.is_authenticated:
            return redirect("shoppingsite:login")
        
        return render(request,self.template,locals())
            
class UpdateProfileView(View):
    template = app + "update_profile.html"

    def get(self,request):
        user = request.user
        category_obj = Category.objects.all()
        userobj = User.objects.get(email=user.email)
        try:
            profileObj = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profileObj = None
        except:
            pass

        return render(request,self.template,locals())
    
    def post(self,request):
        category_obj = Category.objects.all()
        if request.method == 'POST':
            user = request.user
            email = request.POST['email']
            fullName = request.POST['full_name']
            contact = request.POST['contact']
            address = request.POST['address'] 
            bio = request.POST['bio']
            password = request.POST['password']
            profile_picture = request.FILES.get('profile_pic')

            try:
                userobj = User.objects.get(email=user.email)
                userobj.email = email
                userobj.full_name = fullName
                userobj.contact = contact
                userobj.address = address
                
                profile_object = UserProfile.objects.filter(user=user)
                

                if profile_picture is None:
                    picture = ''
                    for i in profile_object:
                        picture = i.profile_pic
                else:
                    picture = profile_picture


                if len(profile_object) == 0:
                    profileobj = UserProfile(user = user,bio = bio, profile_pic = picture)
                    profileobj.save()
                else:
                    for i in profile_object:
                        i.user = user
                        i.profile_pic = picture
                        i.bio = bio
                        i.save()


                if len(password)>0 :
                    userobj.set_password(password)
                    messages.success(request,"Password Changed Successfully")
                
                userobj.save()
                return redirect("shoppingsite:profile")
                
            except:
                messages.error(request,"Error in Updating Profile")
        return render(request,self.template,locals())


# class showCategoryViews(View):
#     model = Category
#     template = app + "allcategories.html"

#     def get(self,request):
#         category_obj = self.model.objects.all()
    
#         return render(request,self.template,locals())

class showProductsViews(View):
    template = app + "productsofcategory.html"
    
    def get(self,request,c_name):
        user = request.user
        subscription_user = UserSubscription.objects.filter(user = user)
        s_user_length = subscription_user.count()
        category_obj = Category.objects.all()
        products_for_this_category = AudioBook.objects.filter(category__title = c_name)
        return render(request,self.template,locals())
    
class ProductDetailsView(View):
    model = AudioBook
    template = app + "product_details.html"

    def get(self,request,p_id):
        user = request.user
        cart_obj = Cart.objects.filter(products__id = p_id)
        category_obj = Category.objects.all()
        product_obj = self.model.objects.get(id = p_id)
        episodes = Episode.objects.filter(audiobook=product_obj).order_by('e_id')
        subscription_user = UserSubscription.objects.filter(user = user)
        s_user_length = subscription_user.count()


        return render(request,self.template,locals())
    
    

class ShowCart(View):
    def get(self,request):
        category_obj = Category.objects.all()
        user = request.user
        if not user.is_authenticated:
            context={'cartItems':[]} 
        else :
            try:
                cartItems = Cart.objects.get(user=user)
                products = {}
                totaloriginalprice = 0
                totalPrice = 0
                for key,value in cartItems.products.items():
                    prd_obj = AudioBook.objects.get(title = str(key))
                    totaloriginalprice += (prd_obj.book_max_price)*value
                    totalPrice += (prd_obj.book_discount_price)*value
                    products[prd_obj] = value
                discount_price = totaloriginalprice-totalPrice
                # taxprice = totalPrice*(3/100)
                # aftertaxprice = totalPrice+taxprice
                
                cartItems.total_price = totalPrice
                cartItems.save()
                
            except Exception:
                products = {}
            
        return render(request,"shoppingsite/cartpage.html",locals())


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product_obj = AudioBook.objects.get(id = product_id)
        product_name = ''
        cart, created = Cart.objects.get_or_create(user=request.user)

    
        products = cart.products or {}
        products[str(product_obj.title)] = products.get(str(product_obj.title), 0) + quantity
        cart.products = products

       
        total_price = sum(AudioBook.objects.get(title=name).book_discount_price * qty for name, qty in products.items())
        cart.total_price = total_price

        cart.save()

        return redirect("shoppingsite:showcart")

    def get(self, request, *args, **kwargs):
        return redirect('home')

        
def RemoveFromCart(request,cart_id,rp_name):
    cart = get_object_or_404(Cart, id=cart_id)
    if str(rp_name) in cart.products:
        if cart.products[str(rp_name)] > 1:
            cart.products[str(rp_name)] -= 1
            cart.save()
        else:
            del cart.products[str(rp_name)]
            cart.save()

    return redirect('shoppingsite:showcart')


class PricingPageView(View):
    template = app + "pricingpage.html"

    def get(self,request):
        category_obj = Category.objects.all()
        subcription_plans = SubscriptionPlan.objects.all()
        features = {}
        for i in subcription_plans:
            subscription_feature = SubscriptionFeatures.objects.filter(sub_plan = i)
            features[i]=list(subscription_feature)
        return render(request,self.template,locals())

class SubscriptionAudioBooks(View):
    model = AudioBook
    template = app + "subscription_products.html"
    def get(self,request):
        category_obj = Category.objects.all()
        user = request.user
        subsc_user_obj = UserSubscription.objects.filter(user = user)
        if subsc_user_obj is not None:
            product_obj = AudioBook.objects.all()

        return render(request,self.template,locals())
        
class SubscribeBooksEpisode(View):
    template = app + "episodesofsubscribebook.html"
    def get(self,request,book_id):
        category_obj = Category.objects.all()
        book_obj = AudioBook.objects.get(id=book_id)
        episodes = Episode.objects.filter(audiobook__in=[book_obj])

        return render(request, self.template,locals())


    
def UserTakeSubscription(request,plan_id):
    user = request.user
    plan_obj = SubscriptionPlan.objects.get(id=plan_id)
    try:
        subs_qset = UserSubscription.objects.filter(user=user,plan=plan_obj).count()
        if subs_qset >0 :
           messages.error(request,"This user already has a subscription to this plan")
           return redirect('shoppingsite:pricing')
        else:
           new_subscription = UserSubscription(user=user,plan=plan_obj)
           new_subscription.save() 
           messages.success(request,'You have successfully subscribed for the selected Plan!')
           return redirect('shoppingsite:home')                    
    except:
        messages.error(request,"Error while Taking Subscription")
        return redirect('shoppingsite:pricing')
    

class Checkout(View):
    template = app + "checkout.html"
    def get(self,request,cart_id):
        user = request.user
        cart = Cart.objects.get(id=cart_id)
        total_price = cart.total_price
        
        return render(request,self.template,locals())

    def post(self,request,cart_id):
        user = request.user
        cart = Cart.objects.get(id=cart_id)
        user_obj = User.objects.get(id = user.id)

        fullName = request.POST['fullName']
        email = request.POST['email']
        #Address
        address = request.POST['address']
        address2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zip']
        country = request.POST['country']
        phone = request.POST['phone']
        #card values
        paymentMethod = request.POST['paymentMethod']
        cc_name = request.POST['cc-name']
        cc_number = request.POST['cc-number']
        cc_expiration = request.POST['cc-expiration']
        cc_cvv = request.POST['cc-cvv']

        order_address = {
            "main_address":address,
            "sub_address":address2,
            "city":city,
            "state":state,
            "zipcode":zipcode,
            "country":country,
            "phone":phone,
        }
        
        try:
            order = Order(user=request.user,products = cart.products,order_value=cart.total_price,payment_type = paymentMethod,address = order_address)
            order.save()
            messages.success(request,"Order Successful!")
            cart.delete()
            return redirect('shoppingsite:home')
        except Exception:
            messages.error(request,"Error while placing Order.")
            return redirect('shoppingsite:checkout',cart_id)
        
    
class DirectBuy(View):
    template = app + "checkout.html"
    def get(self,request,p_id):
        user = request.user
        product_obj = AudioBook.objects.get(id=p_id)
        total_price = product_obj.book_discount_price
        return render(request,self.template,locals())

    def post(self,request,p_id):
        user = request.user
        product_obj = AudioBook.objects.get(id=p_id)
        user_obj = User.objects.get(id = user.id)

        fullName = request.POST['fullName']
        email = request.POST['email']
        #Address
        address = request.POST['address']
        address2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zip']
        country = request.POST['country']
        phone = request.POST['phone']
        #card values
        paymentMethod = request.POST['paymentMethod']
        cc_name = request.POST['cc-name']
        cc_number = request.POST['cc-number']
        cc_expiration = request.POST['cc-expiration']
        cc_cvv = request.POST['cc-cvv']

        order_address = {
            "main_address":address,
            "sub_address":address2,
            "city":city,
            "state":state,
            "zipcode":zipcode,
            "country":country,
            "phone":phone,
        }

        product_dict = {
            product_obj.title:1
        }
        
        try:
            order = Order(user=request.user,products = product_dict,order_value=product_obj.book_discount_price,payment_type = paymentMethod,address = order_address)
            order.save()
            messages.success(request,"Order Successful!")
            return redirect('shoppingsite:home')
        except Exception:
            messages.error(request,"Error while placing Order.")
            return redirect('shoppingsite:productdetails',p_id)


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def remove_audio(request):
    if request.method == 'POST':
        audio_path = request.POST.get('audioPath')
        # Perform validation on audio_path if needed
        # Remove the audio file
        import os
        print(audio_path)
        try:
            audio_obj = Episode.objects.filter(audio_file = audio_path)
            print(audio_obj)
            if os.path.exists(audio_path):
                print("before")
                os.remove(audio_path)
                print("after")
                messages.success(request,{'message': 'Audio file removed successfully'})
            else:
                messages.error(request,{'error': 'Audio file not found'})
        except Exception as e:
            messages.error(request,{'error': str(e)})
    else:
        messages.error(request,{'error': 'Method not allowed'})