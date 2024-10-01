# Generated by Django 5.1.1 on 2024-10-01 09:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0013_quotation2_subject_quotation2_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_name', models.CharField(default='Unknown Employee', max_length=100)),
                ('days_of_duty', models.DecimalField(decimal_places=1, default=0, max_digits=5)),
                ('overtime_days', models.FloatField(default=0)),
                ('total_work_days', models.FloatField(default=0)),
                ('price_per_day', models.FloatField(default=0)),
                ('total_price', models.FloatField(default=0)),
                ('remark', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='days_of_duty',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='employee_name',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='invoice_id',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='overtime_days',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='price_per_day',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='remark',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='total_price',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='total_work_days',
        ),
        migrations.AddField(
            model_name='invoice',
            name='employee_details',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quotation.employeedetails'),
        ),
    ]
