from django.db import models
from django.conf import settings
from app_common.models import Job, User

class Quotation(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    job_title = models.ForeignKey(Job, on_delete=models.CASCADE,null=True, blank=True)
    number_of_persons = models.PositiveIntegerField(null=True, blank=True)
    experience_level = models.CharField(
        max_length=50,
        choices=[
            ('FRESHER', 'FRESHER (Min. 1yr experience)'),
            ('EXPERIENCED', 'Experienced (Min. 5 yrs)')
        ],
        null=True,
        blank=True
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'Quotation {self.id}'

class Item(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='items')
    component = models.CharField(max_length=255, null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    supervisor = models.IntegerField(null=True, blank=True)
    gda = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.component or "Unnamed Component"

class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.item.name} (x{self.quantity})"


class Invoice(models.Model):
    company_name = models.CharField(max_length=255,null=True, blank=True)
    notification_text = models.CharField(max_length=255, null=True, blank=True, default="AS PER LABOUR & ESI DEPARTMENT NOTIFICATION DT. 13.03.2024, GoO")
    semi_skilled = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    unskilled = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    semi_skilled_manpower = models.IntegerField(null=True, blank=True)
    unskilled_manpower = models.IntegerField(null=True, blank=True)
    working_hours = models.IntegerField(null=True, blank=True)
    working_days = models.IntegerField(null=True, blank=True)
    other_allowances_semi_skilled = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    other_allowances_unskilled = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    semi_uniform_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    un_uniform_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    semi_reliever_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    un_reliever_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    semi_operational_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    un_operational_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)


    def __str__(self):
        return self.company_name or 'Invoice'

class Employee(models.Model):
    title = models.CharField(max_length=255)