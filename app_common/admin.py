from django.contrib import admin

from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("id","email")

# @admin.register(models.Category)
# class ProductsAdmin(admin.ModelAdmin):
#     search_fields = ("id","title__icontains")
#     list_display = ("title","id")

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
