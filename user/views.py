from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.views import View
from django.contrib import messages
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from . import forms
# from . import rozerpay
# from app_common.checkout.serializer import CartSerializer,DirectBuySerializer,TakeSubscriptionSerializer,OrderSerializer
from admin_dashboard.order.forms import OrderUpdateForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# from io import StringIO
from django.core.mail import send_mail
import json
from app_common.models import (
    Job,
    Catagory,
    UserProfile,
    User,Application,
    
)

from helpers.utils import dict_filter  # Import dict_filter function
import json

app = "user/"


class HomeView(View):
    template = app + "home1.html"

    def get(self, request):
        return render(request, self.template, locals())
            
        
        user = request.user
        category_obj = Category.objects.all()
        recent_jobs = Job.objects.all().order_by("-id")[:2]
        jobss = Job.objects.all()
        trending_books = JOB.objects.filter(trending = "yes")[:4]
        t_books = []
        e_count = []
        for i in trending_books:
            t_books.append(i)
            e_count.append(Episode.objects.filter(job=i).count())
        booksandepisode = zip(t_books,e_count)
        try:
            user_subscription = get_object_or_404(UserSubscription, user=request.user)
            if user_subscription.days_left() <= 0:
                user_subscription.delete()
        except Exception:
            user_subscription = None


        categories = Category.objects.all()
        products_category_wise = {}
        for category in categories:
            x = []
            product_for_this_category = JOB.objects.filter(category = category)
            x.append(product_for_this_category)
            products_category_wise.update({category.title.replace(" ",""):x})
        category_list = []
        products_list = []
        for i,j in products_category_wise.items():
            category_list.append(i)
            products_list.extend(j)
       
        category_and_products_zip = zip(category_list,products_list)

        return render(request, self.template, locals())


class ProfileView(View):
    template = app + "userprofile.html"

    def get(self, request):
        user = request.user
        print(user)
        catagory_obj =Catagory.objects.all()
        userobj = User.objects.get(email=user.email)
        try:
            profileobj = UserProfile.objects.get(user=userobj)
        except UserProfile.DoesNotExist:
            profileobj = None

        if not user.is_authenticated:
            return redirect("user:login")

        return render(request, self.template, locals())


class UpdateProfileView(View):
    template = app + "update_profile.html"
    form = forms.UpdateProfileForm

    def get(self, request):
        user = request.user
        catagory_obj = Catagory.objects.all()
        userobj = User.objects.get(email=user.email)
        print(userobj)
    
        profileObj, created = UserProfile.objects.get_or_create(user=userobj)
       
        print(profileObj)
        initial_data = {
            "email": userobj.email,
            "full_name": userobj.full_name,
            "contact": userobj.contact,
            "bio": profileObj.bio,
            "profile_pic": profileObj.profile_pic,
            "Resume": profileObj.resume,
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
            skills = form.cleaned_data["skills"]
            profile_picture = form.cleaned_data["profile_pic"]
            password = form.cleaned_data["password"]
            resume = form.cleaned_data["resume"]

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
                    profileobj = UserProfile(user=user, skills=skills, profile_pic=picture)
                    profileobj.save()
                else:
                    for i in profile_object:
                        i.user = user
                        i.profile_pic = picture
                        i.skills = skills
                        i.save()

                
                        
                if len(password) > 0:
                    userobj.set_password(password)
                    messages.success(request, "Password Changed Successfully")

                userobj.save()
                return redirect("user:account_details")

            except:
                messages.error(request, "Error in Updating Profile")
        return render(request, self.template, locals())




# def ADD_USER(request):
#     return render(request,'admin_dashboard/users/add_user.html')

# def ADD_USER_SAVE(request):
#     if request.method != 'POST':
#         return HttpResponse("Method Not Allowed")
#     else:
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         # address = request.POST.get('address')

#         try:
#             user = CustomUser.objects.create_user(username = username,email = email, password = password,first_name = first_name, last_name = last_name, user_type = 2)
#             user.staff.address = address
#             user.save() 
#             messages.success(request,"Successfully Added User")
#             return redirect('add_user')
#         except:
#             messages.error(request,"Failed to Add User")
#             return redirect('add_user')
# class AllAddress(View):
#     template = app + "alladdress.html"

#     def get(self, request):
#         user = request.user
#         address = user.address or []  # This will return a list of addresses

#         return render(request, self.template, {"address": address})


# from uuid import uuid4


# class AddAddress(View):
#     template = app + "addaddress.html"
#     form = forms.AddressForm

#     def get(self, request):
#         form = self.form()
#         return render(request, self.template, locals())

#     def post(self, request):
#         form = self.form(request.POST)
#         if form.is_valid():
#             landmark1 = form.cleaned_data["landmark1"]
#             landmark2 = form.cleaned_data["landmark2"]
#             country = form.cleaned_data["country"]
#             state = form.cleaned_data["state"]
#             city = form.cleaned_data["city"]
#             zipcode = form.cleaned_data["zipcode"]

#             address_id = str(uuid4())

#             address_data = {
#                 "id": address_id,
#                 "landmark1": landmark1,
#                 "landmark2": landmark2,
#                 "country": country,
#                 "state": state,
#                 "city": city,
#                 "zipcode": zipcode,
#             }

#             user = request.user
#             addresses = user.address or []

#             # Append the new address data to the list of addresses
#             addresses.append(address_data)

#             # Save the updated list of addresses back to the user model
#             user.address = addresses
#             user.save()

#             return redirect("user:alladdress")
#         else:
#             return redirect("user:addaddress")


# class DeleteAddress(View):
#     def get(self, request, address_id):
#         user = request.user
#         addresses = user.address or []

#         # Filter out the address with the specified ID
#         addresses = [
#             address for address in addresses if address.get("id") != address_id
#         ]

#         # Update the user model with the modified list of addresses
#         user.address = addresses
#         user.save()

#         return redirect("user:alladdress")


# class showJobsViews(View):
#     template = app + "jobsofcategory.html"

#     def get(self, request, c_name):
#         user = request.user
#         category_obj = Category.objects.all()
#         jobs_for_this_category = Job.objects.filter(category__title=c_name)
#         return render(request, self.template, locals())

# class search_items(View):
#     template = app + "search_item.html"
#     def post(self,request):
#         if request.method == 'POST':
#             user = request.user
#             search_title = request.POST.get("search-box")
#             print(search_title)
#             all_searh_items = []
#             product = Job.objects.filter(title__icontains = search_title)
#             for i in product:
#                 all_searh_items.append(i)
#             category = Job.objects.filter(category__title__icontains=search_title)
#             for j in category:
#                 if j not in all_searh_items:
#                     all_searh_items.append(j)
#             company_name = Job.objects.filter(author__icontains=search_title)
#             for k in company_name:
#                 if k not in all_searh_items:
#                     all_searh_items.append(k)
#             return render(request,self.template,locals())


# def search_product_names(request):
#     if request.method == 'POST':
#         search_term = request.POST.get('search_term', '')
#         if search_term:
#             products = AudioBook.objects.filter(title__icontains=search_term)
#             products_data = [{'id': product.id, 'title': product.title} for product in products]
#             return JsonResponse(products_data, safe=False)
#     return JsonResponse([], safe=False)

# class JobDetailsView(View):
#     model = Job
#     template = app + "product_details.html"

#     def get(self, request, p_id):
#         user = request.user
#         cart_obj = Cart.objects.filter(jobs__id=p_id)
#         category_obj = Category.objects.all()
#         job_obj = self.model.objects.get(id=p_id)
#         # episodes = Episode.objects.filter(job=job_obj).order_by("e_id")
      
#         return render(request, self.template, locals())

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app_common.models import Job, Application
from admin_dashboard.manage_product.forms import ApplicationForm

def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def apply_for_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user
            application.save()
            return redirect('job_list')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_for_job.html', {'form': form, 'job': job})

# class ShowCart(View):
#     def get(self, request):
#         category_obj = Category.objects.all()
#         user = request.user
#         if not user.is_authenticated:
#             context = {"cartItems": []}
#         else:
#             try:
#                 cartItems = Cart.objects.get(user=user)
#                 totaloriginalprice = 0
#                 totalPrice = 0
#                 GST = 0
#                 # Delivary = 0
#                 final_cart_value = 0
#                 products = {}
              
#                 serializer = CartSerializer(cartItems)

#                 obj = serializer.data
#                 print(obj)
#                 for i,j in obj.items():
#                     totaloriginalprice = int(j['gross_cart_value'])
#                     totalPrice = int(j['our_price'])
#                     GST = j['charges']['GST']
#                     # Delivary = j['charges']['Delivary']
#                     final_cart_value = j['final_cart_value']
                
#                 for key, value in cartItems.products.items():
#                     prd_obj = AudioBook.objects.get(title=str(key))
#                     products[prd_obj] = value
#                 discount_price = totaloriginalprice - totalPrice
#                 # taxprice = totalPrice*(3/100)
#                 # aftertaxprice = totalPrice+taxprice

#                 cartItems.total_price = totalPrice
#                 cartItems.save()

#             except Exception as e:
#                 print('Error :', str(e))
#                 products = {}

#         return render(request, "user/cartpage.html", locals())




# class ManageCart(View):
#     model = Cart
 
#     def get(self, request, product_uid):
#         operation_type = request.GET.get('operation')
#         prd_obj = get_object_or_404(AudioBook, uid=product_uid)
#         cart = self.model.objects.get(user = request.user)
#         old_product_dict = cart.products
#         # print(old_product_dict)
#         if prd_obj.title in old_product_dict:
#             if operation_type == 'plus':
#                 old_product_dict[prd_obj.title] += 1
#                 cart.products = old_product_dict
#                 cart.save()
                
 
#             elif operation_type == "min":
#                 old_product_dict[prd_obj.title] -= 1
#                 cart.products = old_product_dict
#                 cart.save()
 
#             # else:
#             #     print("remove operation")
#             #     old_product_dict.pop(product_uid)
#             #     cart.products = old_product_dict
#             #     cart.save()
            
#         else:
#             messages.error(request, "Product is not in your cart..")
#         return redirect('user:showcart')

# def RemoveFromCart(request, cart_id, rp_name):
#     cart = get_object_or_404(Cart, id=cart_id)
#     if str(rp_name) in cart.products:
#         if cart.products[str(rp_name)] > 1:
#             cart.products[str(rp_name)] -= 1
#             cart.save()
#         else:
#             del cart.products[str(rp_name)]
#             cart.save()

#     return redirect("user:showcart")


# class PricingPageView(View):
#     template = app + "pricingpage.html"

#     def get(self, request):
#         category_obj = Category.objects.all()
#         subcription_plans = SubscriptionPlan.objects.all()
#         features = {}
#         for i in subcription_plans:
#             subscription_feature = SubscriptionFeatures.objects.filter(sub_plan=i)
#             features[i] = list(subscription_feature)
#         return render(request, self.template, locals())

# class OrderAudioBooks(View):
#     model = AudioBook
#     template = app + "orderbooks.html"

#     def get(self, request):
#         user = request.user
#         order_user_obj = Order.objects.filter(user=user)
#         products = []
#         for i in order_user_obj:
#             for m,n in i.products.items():
#                 try:
#                     obj = AudioBook.objects.get(title = m)
#                     if obj not in products:
#                         products.append(obj)
#                 except Exception:
#                     pass

#         return render(request, self.template, locals())


# class SubscriptionAudioBooks(View):
#     model = AudioBook
#     template = app + "subscription_products.html"

#     def get(self, request):
#         category_obj = Category.objects.all()
#         user = request.user
#         subsc_user_obj = UserSubscription.objects.filter(user=user)
#         if subsc_user_obj is not None:
#             product_obj = AudioBook.objects.all()

#         return render(request, self.template, locals())


# class SubscribeBooksEpisode(View):
#     template = app + "episodesofsubscribebook.html"

#     def get(self, request, book_id):
#         userId = request.user.id
#         category_obj = Category.objects.all()
#         book_obj = AudioBook.objects.get(id=book_id)
#         episodes = Episode.objects.filter(audiobook__in=[book_obj])

#         return render(request, self.template, locals())

# class SubscriptionChecout(View):
#     model = SubscriptionPlan
#     template = app + "subscription_checkout.html"

#     def get(self,request,plan_id):
#         plan_obj = self.model.objects.get(id=plan_id)
#         plan_serializer = TakeSubscriptionSerializer(plan_obj).data
#         gst = plan_serializer['products_data']['charges']['GST']
#         grandtotal = plan_serializer['products_data']['final_value']
     
#         return render(request,self.template,locals())
    
#     def post(self,request,plan_id):
#         user = request.user
#         plan_obj = SubscriptionPlan.objects.get(id=plan_id)
#         plan_serializer = TakeSubscriptionSerializer(plan_obj).data
#         # Checking whether the user has activate auto renewal
#         auto_renewal = request.POST.get('autoRenewal')

#         ord_meta_data = {}
#         for i,j in plan_serializer.items():
#             ord_meta_data.update(j)
#         t_price = ord_meta_data['final_value']
#         user_address = user.address
#         selected_address = None
#         for address in user_address:
#             selected_address = address
#             break
#         try:
#             subs_qset = UserSubscription.objects.filter(user=user, plan=plan_obj).count()
#             if subs_qset > 0:
#                 messages.error(request, "This user already has a subscription to this plan")
#                 return redirect("user:pricing")
#             else:
#                 if auto_renewal == 'on':
#                     user_email = user.email
#                     subject = "Subscription Taken Successfully"
#                     message = f'Dear {str(user.full_name)},\nYour subscription for {plan_obj.title} and {plan_obj.days} days is taken successfully.\nAlso You Activate Autorenewal for this.'
#                     from_email = "forverify.noreply@gmail.com"
#                     send_mail(subject, message, from_email,[user_email], fail_silently=False)

#                     new_subscription = UserSubscription(user=user, plan=plan_obj,renewal_status = "taken")
#                 else:
#                     user_email = user.email
#                     subject = "Subscription Taken Successfully"
#                     message = f'Dear {str(user.full_name)},\nYour subscription for {plan_obj.title} and {plan_obj.days} days is taken successfully.'
#                     from_email = "forverify.noreply@gmail.com"
#                     send_mail(subject, message, from_email,[user_email], fail_silently=False)

#                     new_subscription = UserSubscription(user=user, plan=plan_obj,renewal_status = "nottaken")
#                 order = Order(
#                     user=user,
#                     full_name=user.full_name,
#                     email=user.email,
#                     products={plan_obj.title:1},
#                     order_value=t_price,
#                     address=selected_address,
#                     order_meta_data = ord_meta_data
#                     # razorpay_payment_id = razorpay_payment_id,
#                     # razorpay_order_id= razorpay_order_id,
#                     # razorpay_signature= razorpay_signature,
#                 )
#                 # order.order_meta_data = json.loads(ord_meta_data)
                
#                 order.save()
#                 new_subscription.save()
#                 messages.success(
#                     request, "You have successfully subscribed for the selected Plan!"
#                 )
#                 return redirect("user:home")
#         except Exception as e:
#             print(e)
#             messages.error(request, "Error while Taking Subscription")
#             return redirect("user:pricing")

    


# class Checkout(View):
#     template = app + "checkout.html"
#     model = Order

#     def get(self, request):
#         user = request.user
#         cart = Cart.objects.get(user=user)
#         order_details = CartSerializer(cart).data
#         total_price = 0
#         for i,j in order_details.items():
#             total_price = float(j['final_cart_value'])
#         user = request.user
#         # addresses = user.address or []
#         # status, rz_order_id = rozerpay.create_order_in_razPay(
#         #     amount=int(cart.total_price)
#         # )
#         # print("over",rz_order_id)

#         context = {
#             "cart": cart.products,
#             # "rz_order_id": rz_order_id,
#             # "api_key": settings.RAZORPAY_API_KEY,
#             "total_price":total_price,
#             # "addresses":addresses
#         }

#         return render(request, self.template, context)
    
# class DirectBuyCheckout(View):
#     template = app + "directbuycheckout.html"

#     def get(self, request,p_id):
#         user = request.user
#         product = AudioBook.objects.get(id=p_id)
#         order_details = DirectBuySerializer(product).data
#         total_price = 0
#         for i,j in order_details.items():
#             total_price = float(j['final_value'])
        
#         user = request.user
#         # addresses = user.address or []
#         # status, rz_order_id = rozerpay.create_order_in_razPay(
#         #     amount=int(cart.total_price)
#         # )
#         # print("over",rz_order_id)

#         context = {
#             # "rz_order_id": rz_order_id,
#             # "api_key": settings.RAZORPAY_API_KEY,
#             "product_uid" : product.uid,
#             "total_price":total_price,
#             # "addresses":addresses
#         }

#         return render(request, self.template, context)




# class UserDownloadInvoice(View):
#     model = Order
#     form_class = OrderUpdateForm
#     template= 'app_common/checkout/invoice.html'

#     def get(self,request, order_uid):
#         order = self.model.objects.get(uid = order_uid)
#         data = OrderSerializer(order).data
#         products = []
#         quantities = []
#         price_per_unit = []
#         total_prices = []
#         for product,p_overview in data['order_meta_data']['products'].items():
#             products.append(product)
#             quantities.append(p_overview['quantity'])
#             price_per_unit.append(p_overview['price_per_unit'])
#             total_prices.append(p_overview['total_price'])
#             # product['product']['quantity']=product['quantity']
#         prod_quant = zip(products, quantities,price_per_unit,total_prices)
#         try:
#             final_total = data['order_meta_data']['final_cart_value']
#         except Exception:
#             final_total = data['order_meta_data']['final_value']
        
#         context ={
#             'order':data,
#             'address':data['address'],
#             'user':order.user,
#             'productandquantity':prod_quant,
#             'GST':data['order_meta_data']['charges']['GST'],
#             'delevery_charge':data['order_meta_data']['charges']['Delivary'],
#             'gross_amt':data['order_meta_data']['our_price'],
#             'discount':data['order_meta_data']['discount_amount'],
#             'final_total':final_total
#         }
#         return render(request,self.template,context)

    
class contactMesage(View):
    template = app + "contact_page.html"

    def get(self,request):
        # initial = {'user': request.user.full_name}
        form = forms.ContactMessageForm

        context={"form":form}
        return render(request,self.template,context)
    
    def post(self,request):
        form = forms.ContactMessageForm(request.POST)  # Instantiate the form with request POST data
        if form.is_valid():  # Add parentheses to is_valid()
            user = form.cleaned_data['user']
            message = form.cleaned_data['message']
            try:
                u_obj = get_object_or_404(User,full_name = user)
                user_email = u_obj.email
                subject = "Your Query Recived."
                message = f"Dear,\nYour Query has been recived successfully.\nOur Team members look into this."
                from_email = "forverify.noreply@gmail.com"
                send_mail(subject, message, from_email,[user_email], fail_silently=False)
                contact_obj = ContactMessage(user = u_obj,message = message)
                contact_obj.save()
                messages.info(request,"Your Message has been sent successfully.")
                return redirect("user:home")
            except Exception as e:
                print (e)
                messages.warning(request,"There was an error while sending your message.")
                return self.get(request)
        else:   # If the form is not valid, re-render the form with errors
            return self.get(request)
        

class AboutPage(View):
    template = app + "about.html"

    def get(self,request):
        
        return render(request,self.template)



class AccountDetails(View):
    template = app + "accountdetails.html"

    def get(self,request):
        user = request.user
        category_obj = Category.objects.all()
        userobj = User.objects.get(id=user.id)
        try:
            profileobj = UserProfile.objects.get(user=userobj)
        except UserProfile.DoesNotExist:
            profileobj = None

        if not user.is_authenticated:
            return redirect("user:login")
        
        return render(request,self.template,locals())
    
# 

class ThankYou(View):
    template = app + "thankyoupage.html"
    def get(self, request):
        return render(request, self.template)

