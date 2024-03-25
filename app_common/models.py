from django.db import models
import io
from PIL import Image
import os
import uuid
from django.core.files import File
from django.core.files.base import ContentFile
from helpers import utils
import datetime
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .manager import MyAccountManager

 
def document_path(self, filename):
    basefilename, file_extension= os.path.splitext(filename)
    myuuid = uuid.uuid4()
    return 'files/{basename}{randomstring}{ext}'.format(basename= basefilename, randomstring= str(myuuid), ext= file_extension)

def generate_random_string():
    random_uuid = uuid.uuid4()
    random_string = random_uuid.hex
    return random_string

def user_logo_path(self, filename):
    basefilename, file_extension= os.path.splitext(filename)
    myuuid = uuid.uuid4()
    return 'user/logo/{basename}{randomstring}{ext}'.format(basename= basefilename, randomstring= str(myuuid), ext= file_extension)

class User(AbstractBaseUser, PermissionsMixin): 
    full_name = models.CharField(max_length= 255, null= True, blank= True)
    password = models.TextField(null=True,blank=True)
    email = models.EmailField(null=True,blank=True,unique=True)

    contact = models.CharField(max_length= 10, null=True, blank=True, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    address = models.JSONField(default= dict, null=True, blank=True) # user_address
    otp = models.CharField(max_length= 10, null=True, blank=True)
    
    # billing details
    USERNAME_FIELD = "email"	
    REQUIRED_FIELDS = ["password"]

    objects = MyAccountManager()

    @property
    def full_contact_number(self):
        if self.contact_number:
            contact_number = '+91' + self.contact_number
        else:
            contact_number='no contact present'

        return contact_number
    
    def get_token(self, *args, **kwargs):
        token= generate_random_string()
        self.token= token
        super().save(*args, **kwargs)
        return token

    def __str__(self):
        return self.email
    

# def banner_image_path(self, filename):
#     basefilename, file_extension= os.path.splitext(filename)
#     myuuid = uuid.uuid4()
#     return 'banner/{basename}{randomstring}{ext}'.format(basename= basefilename, randomstring= str(myuuid), ext= file_extension)

# class Banner(models.Model):
#     YESNO = (
#         ("yes","yes"),
#         ("no","no")
#     )
#     image = models.ImageField(upload_to=banner_image_path, null=True, blank=True)
#     show = models.CharField(max_length=255, choices= YESNO, default= 'yes')
#     sl_no = models.PositiveIntegerField(default=0)

# New Models
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="user_profile_pic/", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

class Category(models.Model):
    YESNO = (
        ("yes","yes"),
        ("no","no")
    )
    title=models.CharField(max_length=255, null=True, blank=True, unique=True)
    description=models.TextField()

    def __str__(self):
        return self.title

class AudioBook(models.Model):
    YESNO = (
        ("yes","yes"),
        ("no","no")
    )
    title = models.CharField(max_length=255, null=True, blank=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    author = models.CharField(max_length=255)
    narrated_by = models.CharField(max_length=100,blank = True,null = True)
    description = models.TextField(blank=True, null=True)
    book_max_price=models.FloatField(default=0.0)
    book_discount_price=models.FloatField(default=0.0)
    release_date = models.DateField()
    demo_audio_file = models.FileField(upload_to='demo_audio/',null=True, blank=True, unique=True)
    language = models.CharField(max_length=50)
    stock=models.IntegerField(default=1)
    trending = models.CharField(max_length= 255, choices= YESNO, default="no") 
    show_as_new = models.CharField(max_length= 255, choices= YESNO ,default="no")
    display_as_bestseller = models.CharField(max_length= 255, choices= YESNO ,default="no")
    hide = models.CharField(max_length= 255, choices= YESNO ,default="no")
    audiobook_image = models.ImageField(upload_to="audiobook_image/", null=True, blank=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    num_ratings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Episode(models.Model):
    e_id = models.PositiveBigIntegerField(null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    audio_file = models.FileField(upload_to='audio/',null=True, blank=True, unique=True)
    audiobook = models.ForeignKey(AudioBook, on_delete=models.CASCADE, related_name='episodes')
    published_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
# class Coupon(models.Model):
#     YESNO = (
#         ("yes","yes"),
#         ("no","no")
#     )
#     DiscountType=(
#         ('pencentage','percentage'),
#         ('flat','flat'),
#         ('freeDelivary','freeDelivary'),
#     )
#     code = models.CharField(max_length=255, unique=True, blank=True, null=True)
#     discount_type = models.CharField(max_length=20, choices= DiscountType, default='flat')
#     quantity = models.PositiveIntegerField(default=0)
#     discount_digit = models.FloatField(default=0.0)
#     active = models.CharField(max_length=10, choices= YESNO, default='yes')



    


# class Products(models.Model):
#     YESNO = (
#         ("yes","yes"),
#         ("no","no")
#     )
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
#     uid=models.CharField(max_length=255, null=True, blank=True)
#     name=models.CharField(max_length=255, null=True, blank=True, unique=True)
#     brand=models.CharField(max_length=255, null=True, blank=True)

#     product_max_price=models.FloatField(default=0.0)
#     product_discount_price=models.FloatField(default=0.0)

#     product_short_description=models.TextField(null=True, blank=True)
#     product_long_description=models.TextField(null=True, blank=True)
#     stock=models.IntegerField(default=1)

#     image = models.ImageField(upload_to="product_image/", null=True, blank=True)
#     trending = models.CharField(max_length= 255, choices= YESNO, default="no") 
#     show_as_new = models.CharField(max_length= 255, choices= YESNO ,default="no")
#     display_as_bestseller = models.CharField(max_length= 255, choices= YESNO ,default="no")
#     hide = models.CharField(max_length= 255, choices= YESNO ,default="no")

#     @property
#     def discount_percentage(self):
#         if self.product_max_price and self.product_discount_price:
#             discount = self.product_max_price - self.product_discount_price
#             percentage = discount / self.product_max_price * 100
#             return int(percentage)


#     def save(self, *args, **kwargs):
#         if not self.uid:
#             self.uid = utils.get_rand_number(5)
#         super().save(*args, **kwargs)


class Cart(models.Model):
    uid=models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.JSONField(default=dict, null=True, blank=True)
    # coupon = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)

    def __str__(self):
        return self.uid

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = utils.get_rand_number(5)
        super().save(*args, **kwargs)

 
class Order(models.Model):
    ORDER_STATUS = (
        ("Placed","Placed"),
        ("Accepted","Accepted"),
        ("Cancel","Cancel"),
        ("On_Way","On_Way"),
        ("Refund","Refund"),
        ("Return","Return"),
    )

    PaymentStatus = (
        ("Paid","Paid"),
        ("Pending","Pending"),
        ("Refunded","Refunded"),
    )

    PaymentMode=(
        ("ONLINE","ONLINE"),
        ("CASH","CASH"),
        ("PENDING","PENDING"),
    )

    uid=models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.JSONField(default=dict, null=True, blank=True)
    coupon = models.CharField(max_length=255, null=True, blank=True)
    order_value = models.FloatField(default=0.0)
    order_meta_data = models.JSONField(default=dict, null=True, blank=True)
    order_status = models.CharField(max_length=255, choices= ORDER_STATUS, default="Placed")
    payment_method = models.CharField(max_length=255, choices= PaymentMode, default="PENDING")
    payment_status = models.CharField(max_length=255, choices= PaymentStatus, default="Paid")

    address = models.JSONField(default=dict, null=True, blank=True)

    more_info = models.TextField(null= True, blank=True)
    date = models.DateField(auto_now_add= True, null=True, blank=True)

    transaction_id = models.TextField(null= True, blank=True)
    can_edit = models.BooleanField(default=True) # id a order is canceled or refunded, make it non editable

    def __str__(self):
        return self.uid

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = utils.get_rand_number(5)
        super().save(*args, **kwargs)


 
class ContactMessage(models.Model):
    STATUS = (
        ("pending","pending"),
        ("read","read"),
        ("resolved","resolved"),
    )
    uid=models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE, null= True, blank= True)
    order_number = models.CharField(max_length=255, null= True, blank= True)
    message = models.TextField(null= True, blank= True)
    status = models.CharField(max_length=255,choices=STATUS, default= 'new')
    reply = models.TextField(null=True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = utils.get_rand_number(5)
        super().save(*args, **kwargs)

# class Offers(models.Model):
#     product = models.ForeignKey(Products, on_delete= models.CASCADE, null= True, blank= True)
#     title = models.TextField(null=True, blank= True)
#     escription = models.TextField(null=True, blank= True)
        
class SubscriptionPlan(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    days = models.IntegerField(default=30)

    def __str__(self):
        return f"{self.title}\t{self.days} days"
    
class SubscriptionFeatures(models.Model):
    sub_plan = models.ForeignKey(SubscriptionPlan,on_delete = models.CASCADE)
    feature = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.feature}"

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)

    def calculate_end_date(self):
        return self.start_date + timedelta(days=self.plan.days)

    @property
    def end_date(self):
        return self.calculate_end_date()