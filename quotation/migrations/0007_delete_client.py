# Generated by Django 5.0.7 on 2024-09-13 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0006_quotation_create_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Client',
        ),
    ]
