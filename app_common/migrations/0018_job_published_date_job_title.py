# Generated by Django 4.2 on 2024-06-24 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_common', '0017_alter_contactmessage_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
