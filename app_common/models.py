from django.db import models
import io
# from PIL import Image
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
from django.core.mail import send_mail
from django.core.validators import RegexValidator

 
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


class Catagory(models.Model):

    title=models.CharField(max_length=255, null=True, blank=True, unique=True)
    description=models.TextField()

    def __str__(self):
        return self.title
        
class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length= 255, null= True, blank= True)
    email = models.EmailField(null=True,blank=True,unique=True)
    password = models.TextField(null=True,blank=True)
    contact = models.CharField(max_length= 10, null=True, blank=True)
    catagory = models.ForeignKey(Catagory, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
 
    wallet = models.FloatField(default=0.0)
   
    token = models.CharField(max_length=100, null=True, blank=True)
 
    # we are storing some extra data in the meta data field
    meta_data = models.JSONField(default= dict)
   
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

 
# New Models
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(default='')
    profile_pic = models.ImageField(upload_to="user_profile_pic/", null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    resume = models.FileField(upload_to="user_resume/", null=True, blank=True)
    
    
    




class Job(models.Model):

    FULL_TIME = 'Full-Time'
    PART_TIME = 'Part-Time'
    CONTRACT = 'Contract'
    INTERNSHIP = 'Internship'
    
    JOB_TYPE_CHOICES = [
        (FULL_TIME, 'Full-Time'),
        (PART_TIME, 'Part-Time'),
        (CONTRACT, 'Contract'),
        (INTERNSHIP, 'Internship'),
    ]
    STATUS_CHOICES = [
        ('unpublished', 'Unpublished'),
        ('published', 'Published'),
    ]


    title = models.CharField(max_length=255, null=True, blank=True)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, limit_choices_to={'is_staff': True})
    catagory = models.ForeignKey(Catagory, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.CharField(max_length =300,blank=True, null=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    posted_at = models.DateField(default=timezone.now)
    published_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    company_name = models.CharField(max_length=255, default='Default Company')
    company_website = models.URLField(blank=True, null=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    vacancies = models.PositiveIntegerField(default=1)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default=FULL_TIME)
    status = models.CharField(max_length=15 , choices=STATUS_CHOICES, default='unpublished')
   
        
    def __str__(self):
        return self.title
 
    

class Application(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Interviewed', 'Interviewed'),
        ('Hired', 'Hired'),
        ('Rejected', 'Rejected'),
     ]
     
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(default='')
    contact = models.IntegerField(null=True, blank=True, unique=True, default=0)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Applied')
        
    @property
    def user_full_name(self):
        return self.user.get_full_name()

    @property
    def user_email(self):
        return self.user.email

    @property
    def user_contact(self):
        return self.user.profile.contact_number 

    def __str__(self):
        return f'{self.user.full_name} applied for {self.job.catagory} ' 
    


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

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employer = models.ForeignKey(User, related_name='employees', on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    period_start = models.DateField()
    period_end = models.DateField()
    docs = models.FileField(upload_to='employee_docs/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.email

class CommunicationLog(models.Model):
    candidate = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    medium = models.CharField(max_length=10)  # 'whatsapp' or 'sms'

    def __str__(self):
        return f"Message to {self.User.first_name} at {self.sent_at}"


class Edit_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    skills = models.TextField(max_length=500, blank=True, null=True)
    def __str__(self):
        return self.user.username


