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
from django.core.mail import send_mail

 
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
    email = models.EmailField(null=True,blank=True,unique=True)
    password = models.TextField(null=True,blank=True)
    contact = models.CharField(max_length= 10, null=True, blank=True)
 
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
 
   


    # @property
    # def full_contact_number(self):
    #     if self.contact_number:
    #         contact_number = '+91' + self.contact_number
    #     else:
    #         contact_number='no contact present'

    #     return contact_number
    
    # def get_token(self, *args, **kwargs):
    #     token= generate_random_string()
    #     self.token= token
    #     super().save(*args, **kwargs)
    #     return token

    # def __str__(self):
    #     return self.email

    def send_reset_password_email(self):
        token = self.generate_reset_password_token()
        reset_link = f"http://35.154.55.245/reset-password/{token}/"
        subject = 'Reset your password'
        message = f'Hi {self.full_name},\n\nTo reset your password, please click the link below:\n\n{reset_link}\n\nIf you did not request this, please ignore this email.'
        send_mail(subject, message, 'noreplyf577@gmail.com', [self.email])
       
       
       
    def generate_reset_password_token(self):
        token = str(uuid.uuid4())
        self.token = token
        self.save()
        return token
   
    def reset_password(self, token, new_password):
        # Check if the token is valid (you may want to implement token validation logic here)
        if self.token == token:
            # Set the new password and save the user
            self.set_password(new_password)
            self.token = None  # Clear the token after password reset
            self.save()
            return True
        else:
            return False   

# New Models
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(default='')
    profile_pic = models.ImageField(upload_to="user_profile_pic/", null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    resume = models.ImageField(upload_to="user_resume/", null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, default='applied')  # statuses: applied, interviewed, hired, etc.
    
    def __str__(self):
        return 

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
    candidates = models.ManyToManyField(UserProfile, related_name='job_posts')

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


# class Employee(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     position = models.CharField(max_length=100)
#     department = models.CharField(max_length=100)

#     def __str__(self):
#         return self.user.username

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


class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(default='')
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')
    category = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, default='applied')  # statuses: applied, interviewed, hired, etc.

    def __str__(self):
        return f"{self.first_name} {self.last_name}"