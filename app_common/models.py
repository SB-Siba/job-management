from django.db import models
import os
import uuid
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import MyAccountManager

# Utility Functions
def document_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    myuuid = uuid.uuid4()
    return f'files/{basefilename}{myuuid}{file_extension}'

def generate_random_string():
    return uuid.uuid4().hex

def user_logo_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    myuuid = uuid.uuid4()
    return f'user/logo/{basefilename}{myuuid}{file_extension}'

# Models
class Category(models.Model):
    title = models.CharField(max_length=255, unique=True, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title

class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=10, null=True, blank=True, validators=[RegexValidator(r'^\d{10}$')])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    wallet = models.FloatField(default=0.0)
    token = models.CharField(max_length=100, null=True, blank=True)
    meta_data = models.JSONField(default=dict)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = MyAccountManager()

    @property
    def full_contact_number(self):
        return f'+91{self.contact}' if self.contact else 'No contact present'

    def get_token(self, *args, **kwargs):
        self.token = generate_random_string()
        super().save(*args, **kwargs)
        return self.token

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="user_profile_pic/", null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    resume = models.FileField(upload_to="user_resume/", null=True, blank=True)

    def __str__(self):
        return self.user.email

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
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'is_staff': True})
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=300, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    posted_at = models.DateField(default=timezone.now)
    published_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    company_name = models.CharField(max_length=255, default='Default Company')
    company_website = models.URLField(null=True, blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    vacancies = models.PositiveIntegerField(default=1)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default=FULL_TIME)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='unpublished')

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
    contact = models.CharField(max_length=10, null=True, blank=True, validators=[RegexValidator(r'^\d{10}$')])
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Applied')

    @property
    def user_full_name(self):
        return self.user.full_name

    @property
    def user_email(self):
        return self.user.email

    @property
    def user_contact(self):
        return self.user.contact

    def __str__(self):
        return f'{self.user.full_name} applied for {self.job.title}'

class ContactMessage(models.Model):
    STATUS = (
        ("pending", "pending"),
        ("read", "read"),
        ("resolved", "resolved"),
    )

    uid = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS, default='pending')
    reply = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = generate_random_string()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user if self.user else 'Anonymous'} - {self.status}"

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employer = models.ForeignKey(User, related_name='employees', on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    docs = models.FileField(upload_to='employee_docs/', null=True, blank=True)

    def __str__(self):
        return self.user.full_name or self.user.email

class CommunicationLog(models.Model):
    candidate = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    medium = models.CharField(max_length=10)  # 'whatsapp' or 'sms'

    def __str__(self):
        return f"Message to {self.candidate.user.email} at {self.sent_at}"

class EditUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    skills = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.user.email
