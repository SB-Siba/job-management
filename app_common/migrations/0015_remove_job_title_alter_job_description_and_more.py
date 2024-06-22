# Generated by Django 4.2 on 2024-06-22 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_common', '0014_rename_publish_until_job_expiry_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='title',
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='requirements',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
