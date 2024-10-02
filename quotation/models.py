from datetime import datetime
import json
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

class Quotation2(models.Model):
    company_name = models.CharField(max_length=255, null=True, blank=True)
    vendor_name = models.CharField(max_length=255,null=True, blank=True)
    post1 = models.CharField(max_length=255, null=True, blank=True)
    post2 = models.CharField(max_length=255, null=True, blank=True)
    notification_text = models.CharField(max_length=255, null=True, blank=True, default="AS PER LABOUR & ESI DEPARTMENT NOTIFICATION DT. 13.03.2024, GoO")
    semi_skilled = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    unskilled = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    skilled = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    high_skilled = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    semi_skilled_manpower = models.IntegerField(null=True, blank=True)
    unskilled_manpower = models.IntegerField(null=True, blank=True)
    skilled_manpower = models.IntegerField(null=True, blank=True)
    high_skilled_manpower = models.IntegerField(null=True, blank=True)

    working_hours = models.IntegerField(null=True, blank=True)
    working_days = models.IntegerField(null=True, blank=True)

    other_allowances_semi_skilled = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    other_allowances_unskilled = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    other_allowances_skilled = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    other_allowances_high_skilled = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    semi_uniform_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    un_uniform_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    skilled_uniform_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    high_skilled_uniform_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    semi_reliever_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    un_reliever_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    skilled_reliever_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    high_skilled_reliever_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    semi_operational_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    un_operational_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    skilled_operational_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    high_skilled_operational_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    to = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.company_name or 'Invoice'

class EmployeeDetails(models.Model):
    employee_name = models.CharField(max_length=100, default='Unknown Employee')
    days_of_duty = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    overtime_days = models.FloatField(default=0)
    total_work_days = models.FloatField(default=0)
    price_per_day = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    remark = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.employee_name 

class Invoice(models.Model):
    invoice_detail_id = models.AutoField(primary_key=True)
    employee_details = models.JSONField(default=list, null=True, blank=True)  # Use JSONField to store multiple employee details
    company_name = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    esi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    epf = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    invoice_number = models.CharField(max_length=255, unique=True, blank=True, null=True)  # Invoice number field

    def __str__(self):
        return f"Invoice {self.invoice_number if self.invoice_number else self.invoice_detail_id}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        super(Invoice, self).save(*args, **kwargs)

    def generate_invoice_number(self):
        current_year = datetime.now().year
        next_year = current_year + 1
        financial_year = f"{str(current_year)[-2:]}-{str(next_year)[-2:]}"
        
        # Get the latest invoice by invoice_detail_id
        latest_invoice = Invoice.objects.order_by('-invoice_detail_id').first()
        
        if latest_invoice and latest_invoice.invoice_number:
            last_number = int(latest_invoice.invoice_number.split('/')[-1])
            serial_number = str(last_number + 1).zfill(3)
        else:
            serial_number = '001'

        return f"PR/INVOICE/{financial_year}/{serial_number}"