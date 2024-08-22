from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.company_name or self.name or "Unnamed Client"

class Quotation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'Quotation {self.id} for {self.client}'

class Item(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='items')  # Foreign key relationship
    sr_no = models.PositiveIntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:  # Only set sr_no on new items
            last_item = Item.objects.order_by('-sr_no').first()
            self.sr_no = (last_item.sr_no + 1) if last_item else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or "Unnamed Item"

class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.item.name} (x{self.quantity})"


class Invoice(models.Model):
    company_name = models.CharField(max_length=255,null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    contact = models.CharField(max_length=20,null=True, blank=True)

class Job(models.Model):
    title = models.CharField(max_length=255)

class Employee(models.Model):
    title = models.CharField(max_length=255)