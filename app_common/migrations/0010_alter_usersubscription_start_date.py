# Generated by Django 5.0.3 on 2024-03-23 12:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_common', '0009_subscriptionplan_subscriptionfeatures_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubscription',
            name='start_date',
            field=models.DateField(default=datetime.date(2024, 3, 23)),
        ),
    ]
