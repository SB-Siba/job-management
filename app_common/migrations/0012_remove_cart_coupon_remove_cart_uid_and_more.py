# Generated by Django 5.0.3 on 2024-03-25 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_common', '0011_remove_usersubscription_end_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='coupon',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='uid',
        ),
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
