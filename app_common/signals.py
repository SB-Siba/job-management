# admin_dashboard/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import (
Application,
Employee)
@receiver(post_save, sender=Application)
def create_employee(sender, instance, **kwargs):
    if instance.status == 'Hired':
        Employee.objects.get_or_create(
            user=instance.user,
            employer=instance.job.client,
            defaults={
                'salary': 0,  # Default or initial values
                'period_start': timezone.now(),
                'period_end': timezone.now() + timezone.timedelta(days=365),
            }
        )
