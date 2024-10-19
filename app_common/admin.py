from django.contrib import admin
# from django import forms
from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("id","email")

@admin.register(models.Category)
class categoryAdmin(admin.ModelAdmin):
    search_fields = ("id","title__icontains")
    list_display = ("title","id")

@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'salary', 'period_start', 'period_end')
    search_fields = ('user__full_name', 'user__email', 'employer__full_name', 'employer__email')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'salary', 'period_start', 'period_end')
        }),
        ('Documents', {
            'fields': ('docs',),
        }),
    )
# class JobForm(forms.ModelForm):
#     class Meta:
#         model = Job
#         fields = '__all__'
#         widgets = {
#             'publish_until': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#         }

@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('category', 'company_name', 'location', 'vacancies',  'posted_at', 'updated_at')
    list_filter = ('category','location')
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
    search_fields = ('user_full_name', 'user_email', 'user_contact', 'job__title')
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.status == 'Hired':
            Employee.objects.get_or_create(
                user=obj.user,
                employer=obj.job.client,
                defaults={
                    'salary': 0,  # Default or initial values
                    'period_start': timezone.now(),
                    'period_end': timezone.now() + timezone.timedelta(days=365),
                }
            )


@admin.register(models.ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    search_fields = ("uid", "name", "email", "user__full_name")
    list_display = ("uid", "id", "get_name", "get_email", "status", "created_at")
    
    def get_name(self, obj):
        return obj.user.full_name if obj.user else obj.name
    get_name.short_description = 'Name'
    
    def get_email(self, obj):
        return obj.user.email if obj.user else obj.email
    get_email.short_description = 'Email'