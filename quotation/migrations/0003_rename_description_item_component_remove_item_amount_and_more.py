# Generated by Django 5.0.7 on 2024-09-13 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0002_remove_invoice_issued_at_remove_invoice_paid_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='description',
            new_name='component',
        ),
        migrations.RemoveField(
            model_name='item',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='item',
            name='name',
        ),
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='item',
            name='sr_no',
        ),
        migrations.AddField(
            model_name='item',
            name='gda',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='supervisor',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
