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
    UserSubscription
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


        return render(request,self.template,locals())
    

def play_audio_demo(request, audio_id):
    audio_file = get_object_or_404(AudioBook, pk=audio_id)
    return FileResponse(audio_file.demo_audio_file, content_type='audio/mp3')

def play_audio_episodes(request, audio_id):
    audio_file = get_object_or_404(Episode, pk=audio_id)
    return FileResponse(audio_file.audio_file, content_type='audio/mp3')
    

class ShowCart(View):
    def get(self,request):
        category_obj = Category.objects.all()
        user = request.user
        if not user.is_authenticated:
            context={'cartItems':[]} 
        else :
            cartItems = Cart.objects.filter(user=user)
            cart_product_names = [i.products['product'] for i in cartItems]
            cart_product_objs = [AudioBook.objects.get(title=j) for j in cart_product_names]
            cart_prod =  [i.products for i in cartItems]
            
            totaloriginalprice = sum([float(m.book_max_price) for m in cart_product_objs]) 
            totalPrice = sum([float(m.products['price'])*int(m.quantity) for m in cartItems])
            discount_price = totaloriginalprice-totalPrice
            taxprice = totalPrice*(3/100)
            aftertaxprice = totalPrice+taxprice

            context={
                'cartItems':cartItems,
                'category_obj':category_obj,
                "totalPrice":totalPrice,
                "aftertaxprice":aftertaxprice,
                "totaloriginalprice":totaloriginalprice,
                "discount_price":discount_price,

                }
            
        return render(request,"shoppingsite/cartpage.html",context)


class AddToCartView(View):
    def get(self, request, product_id):
        try:
            # Get 9the product by ID
            product = AudioBook.objects.get(id=product_id)
            print (product)
            
            # Check if the product exists
            if product:
                # Filter the product attributes for the cart
                product_dict = dict_filter(product.__dict__, ['title', 'book_max_price', 'book_discount_price','audiobook_image'])
                product_dict['book_discount_price'] = str(product_dict['book_discount_price'])
                product_dict['quantity'] = 1
                
                # Get the user's cart or create a new one if it doesn't exist
                cart, created = Cart.objects.get_or_create(user=request.user)
                
                if created:
                    # Create a new cart and add the product
                    cart.products = json.dumps({str(product_id): product_dict})
                    cart.total_price = product.book_discount_price
                    cart.quantity = 1
                    cart.save()
                    messages.success(request, "Product added to cart successfully")
                else:
                    # Update existing cart with the new product
                    cart_items_dict = json.loads(cart.products)
                    
                    if str(product_id) in cart_items_dict:
                        cart_items_dict[str(product_id)]['quantity'] += 1
                    else:
                        cart_items_dict[str(product_id)] = product_dict
                        
                    cart.product_list = json.dumps(cart_items_dict)
                    cart.total_price += product.price
                    cart.quantity += 1
                    cart.save()
                    messages.success(request, "Product added to cart successfully")
                    
                return redirect('shoppingsite:showcart')
            else:
                messages.error(request, "Product not found")
                return redirect('shoppingsite:home')
        except AudioBook.DoesNotExist:
            messages.error(request, "Product not found")
            return redirect('shoppingsite:showcart')
        except Exception as e:
            print(e)
            messages.error(request, f"Failed to add product to cart: {str(e)}")
            # You can customize this further based on your error handling requirements
            return render(request, 'error.html', {'error_message': str(e)})


# class AddToCart(View):
#     def post(self,request):
#         category_obj = Category.objects.all()
#         user = request.user
#         product_id = request.POST.get("product_id")
#         try:
#             product_obj = AudioBook.objects.get(id = product_id)
#             cartobj = Cart.objects.filter(user=user)
#             if cartobj:
                
#                     v = Cart.products
#                     if v["product"] == product_obj.title:
#                         quantity = int(v["quantity"]) + 1
#                         print(quantity,i)
#                         new_data = {
#                             "id":product_obj.id,
#                             "product" : product_obj.title ,
#                             "price" : product_obj.book_discount_price,
#                             "quantity" : quantity,
#                         }

#                         products.update(new_data)
#                         i.save()    
#                         return redirect("shoppingsite:showcart")
#                     else:
#                         # data = {
#                         #     "id":product_obj.id,
#                         #     "product" : product_obj.title ,
#                         #     "price" : product_obj.book_discount_price,
#                         #     "quantity" : 1,
#                         # }
#                         # products.(data)
#                         # i.save()
#                         # print(i)
#                         # return redirect("shoppingsite:showcart")
#             else:
#                 prodc = {
#                     'product':product_obj.title,
#                     'price':product_obj.book_discount_price,
#                     'quantity':1,
#                 }
                
#                 adtocartobj = Cart.objects.create(uid = user.id,user = user,products = prodc,quantity = 1)
#                 adtocartobj.save()
#                 messages.success(request,"Product Added To Cart Successfully")
#                 return redirect("shoppingsite:showcart")
#         except Exception as e:
#             print(e)
#             product_obj = AudioBook.objects.get(id = product_id)
#             messages.error(request,'Product Not Found')
#             return redirect("shoppingsite:productdetails",product_id)
        
def RemoveFromCart(request,rp_id):
    cartItemObj = Cart.objects.filter(pk=rp_id)
    for i in cartItemObj:
        if i.quantity > 1:
            i.quantity -= 1
            i.save()
        else:
            i.delete()
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