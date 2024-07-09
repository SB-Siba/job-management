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
    list_display = ('catagory', 'company_name', 'location', 'vacancies',  'posted_at', 'updated_at')
    list_filter = ('catagory','location')
    search_fields = ('title', 'description', 'location', 'company_name')
    actions = ['publish_jobs', 'unpublish_jobs']

    def publish_jobs(self, request, queryset):
        queryset.update(published=True)
    publish_jobs.short_description = 'Publish selected jobs'

    def unpublish_jobs(self, request, queryset):
        queryset.update(published=False)
    unpublish_jobs.short_description = 'Unpublish selected jobs'

@admin.action(description='Mark selected candidates as Hired')
def make_hired(modeladmin, request, queryset):
    queryset.update(status='Hired')
    
@admin.register(models.Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'user_full_name', 'user_email','user_contact', 'applied_at','status')
    actions = [make_hired]
    list_filter = ('status', 'job')
    search_fields = ('user_full_name', 'user_email', 'user_contact', 'job__catagory')
 


@admin.register(models.ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    search_fields = ("uid",)
    list_display = ("uid","id","email", "created_at")

    def email(self, obj):
        return obj.email
    email.short_description = 'Email'