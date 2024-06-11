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

# @admin.register(models.AudioBook)
# class ProductsAdmin(admin.ModelAdmin):
#     search_fields = ("id","title__icontains")
#     list_display = ("id","title","author")

# @admin.register(models.Cart)
# class CartAdmin(admin.ModelAdmin):
#     search_fields = ("user__id", "id",)
#     list_display = ("user","id")


# @admin.register(models.Order)
# class OrderAdmin(admin.ModelAdmin):
#     search_fields = ("uid",)
#     list_display = ("uid","id",)

# @admin.register(models.ContactMessage)
# class ContactMessageAdmin(admin.ModelAdmin):
#     search_fields = ("uid",)
#     list_display = ("uid","id",)
