from django.contrib import admin
# from django import forms
from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("id","email")

@admin.register(models.Catagory)
class CatagoryAdmin(admin.ModelAdmin):
    search_fields = ("id","title__icontains")
    list_display = ("title","id")


# class JobForm(forms.ModelForm):
#     class Meta:
#         model = Job
#         fields = '__all__'
#         widgets = {
#             'publish_until': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#         }

@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('catagory', 'company_name', 'location', 'vacancies', 'published', 'posted_at', 'updated_at')
    list_filter = ('published', 'location')
    search_fields = ('title', 'description', 'location', 'company_name')
    actions = ['publish_jobs', 'unpublish_jobs']

    def publish_jobs(self, request, queryset):
        queryset.update(published=True)
    publish_jobs.short_description = 'Publish selected jobs'

    def unpublish_jobs(self, request, queryset):
        queryset.update(published=False)
    unpublish_jobs.short_description = 'Unpublish selected jobs'

    
@admin.register(models.Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'user_full_name', 'user_email','user_contact', 'applied_at')
    search_fields = ('user_full_name', 'user_email', 'user_contact', 'job__title')
    def get_user_full_name(self, obj):
        return obj.user.get_full_name()
    get_user_full_name.short_description = 'Full Name'
    
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email'
    
    def get_user_contact(self, obj):
        return obj.user.profile.contact_number  # Adjust as per your profile model
    get_user_contact.short_description = 'Contact Number'


@admin.register(models.ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    search_fields = ("uid",)
    list_display = ("uid","id",)
