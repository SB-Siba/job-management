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
from django.db.models.signals import post_save
from django.dispatch import receiver
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

    is_client = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    address = models.JSONField(default= dict, null=True, blank=True)
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
    

def banner_image_path(self, filename):
    basefilename, file_extension= os.path.splitext(filename)
    myuuid = uuid.uuid4()
    return 'banner/{basename}{randomstring}{ext}'.format(basename= basefilename, randomstring= str(myuuid), ext= file_extension)

class Banner(models.Model):
    YESNO = (
        ("yes","yes"),
        ("no","no")
    )
    image = models.ImageField(upload_to=banner_image_path, null=True, blank=True)
    show = models.CharField(max_length=255, choices= YESNO, default= 'yes')
    sl_no = models.PositiveIntegerField(default=0)

# New Models
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="user_profile_pic/", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    resume = models.ImageField(upload_to="user_resume/", null=True, blank=True)

class Catagory(models.Model):
    YESNO = (
        ("yes","yes"),
        ("no","no")
    )
    title=models.CharField(max_length=255, null=True, blank=True, unique=True)
    description=models.TextField()

    def __str__(self):
        return self.title



class Job(models.Model):
    YESNO = (
        ("yes","yes"),
        ("no","no")
    )
    uid=models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True, unique=True)
    catagory = models.ForeignKey(Catagory, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, null=True, blank=True, unique=True)
    posted_at = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = utils.get_rand_number(5)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = utils.get_rand_number(5)
        
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.user.username} - {self.job.title}'
    
 

 
class ContactMessage(models.Model):
    STATUS = (
        ("pending","pending"),
        ("read","read"),
        ("resolved","resolved"),
    )
    uid=models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE, null= True, blank= True)
    # order_number = models.CharField(max_length=255, null= True, blank= True)
    message = models.TextField(null= True, blank= True)
    status = models.CharField(max_length=255,choices=STATUS, default= 'new')
    reply = models.TextField(null=True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = utils.get_rand_number(5)
        super().save(*args, **kwargs)
