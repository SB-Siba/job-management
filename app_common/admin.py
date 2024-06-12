from django.contrib import admin

from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("id","email")

@admin.register(models.Catagory)
class ProductsAdmin(admin.ModelAdmin):
    search_fields = ("id","title__icontains")
    list_display = ("title","id")

@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'posted_at')
    search_fields = ('title', 'location')

@admin.register(models.Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'user', 'status', 'applied_at')
    search_fields = ('job__title', 'user__username')
    list_filter = ('status',)



@admin.register(models.ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    search_fields = ("uid",)
    list_display = ("uid","id",)
