# Generated by Django 4.2 on 2024-07-04 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_common', '0010_remove_userprofile_catagory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='client',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(choices=[('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'), ('Contract', 'Contract'), ('Internship', 'Internship')], default='Full-Time', max_length=20),
        ),
    ]
