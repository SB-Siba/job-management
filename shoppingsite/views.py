from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from django.views import View
from django.contrib import messages
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from app_common.models import (
    AudioBook,
    Category,
    Cart,
    UserProfile,
    User,
    Episode
)
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
        category_obj = Category.objects.all()
        products_for_this_category = AudioBook.objects.filter(category__title = c_name)
        return render(request,self.template,locals())
    
class ProductDetailsView(View):
    model = AudioBook
    template = app + "product_details.html"

    def get(self,request,p_id):
        cart_obj = Cart.objects.filter(products__id = p_id)
        category_obj = Category.objects.all()
        product_obj = self.model.objects.get(id = p_id)
        episodes = Episode.objects.filter(audiobook=product_obj).order_by('e_id')

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
            totaloriginalprice = sum([float(m.products.book_max_price)*int(m.quantity) for m in cartItems]) 
            totalPrice = sum([float(m.products.book_discount_price)*int(m.quantity) for m in cartItems])
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
    
class AddToCart(View):
    def post(self,request):
        category_obj = Category.objects.all()
        user = request.user
        product_id = request.POST.get("product_id")
        try:
            product_obj = AudioBook.objects.get(id = product_id)
            cartobj = Cart.objects.filter(products=product_obj)
            print(cartobj[0].quantity)
            if len(cartobj)>0:
                qty = int(cartobj[0].quantity)+1
                obj = cartobj[0]
                obj.quantity = qty
                obj.save()
                return redirect("shoppingsite:showcart")
            else:
                adtocartobj = Cart(uid = user.id,user = user,products = product_obj)
                adtocartobj.save()
                messages.success(request,"Product Added To Cart Successfully")
                return redirect("shoppingsite:showcart")
        except Exception:
            product_obj = AudioBook.objects.get(id = product_id)
            messages.error(request,'Product Not Found')
            return redirect("shoppingsite:productdetails",product_id)
        
def RemoveFromCart(request,rp_id):
    cartItemObj = Cart.objects.filter(pk=rp_id)
    for i in cartItemObj:
        if i.quantity > 1:
            i.quantity -= 1
            i.save()
        else:
            i.delete()
    return redirect('shoppingsite:showcart')


class SubscriptionAudioBooks(View):
    model = AudioBook
    template = app + "subscription_products.html"
    def get(self,request):
        product_obj = AudioBook.objects.all()

        return render(request,self.template,locals())
        
class SubscribeBooksEpisode(View):
    template = app + "episodesofsubscribebook.html"
    def get(self,request,book_id):
        book_obj = AudioBook.objects.get(id=book_id)
        episodes = Episode.objects.filter(audiobook__in=[book_obj])

        return render(request, self.template,locals())

