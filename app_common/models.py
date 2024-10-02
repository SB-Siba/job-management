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
    resume = models.FileField(upload_to='user_resume/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)


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
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=300, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    posted_at = models.DateField(default=timezone.now)
    published_date = models.DateTimeField(default=timezone.now) 
    expiry_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(null=True, blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    vacancies = models.PositiveIntegerField(default=1)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default=FULL_TIME)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='unpublished')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

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
    user_resume = models.FileField(upload_to='user_resume/', null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Applied')
    hiring_date = models.DateField(auto_now_add=True, null=True, blank=True)
    hiring_time = models.TimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == 'Hired' and (not self.hiring_date or not self.hiring_time):
            self.hiring_date = timezone.now().date()
            self.hiring_time = timezone.now().time()
        super(Application, self).save(*args, **kwargs)

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
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = generate_random_string()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user if self.user else 'Anonymous'} - {self.status}"

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employer')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    docs = models.FileField(upload_to='employee_docs/', null=True, blank=True)

    class Meta:
        unique_together = ('user', 'job', 'employer')

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
class EmployeeReplacementRequest(models.Model):
    client_email = models.EmailField()
    current_employee = models.EmailField()
    new_employee_name = models.CharField(max_length=255)
    new_employee_email = models.EmailField()
    new_employee_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='Pending')  # Status field to track the request status

    def __str__(self):
        return f"Request from {self.client_email} to replace {self.current_employee}"