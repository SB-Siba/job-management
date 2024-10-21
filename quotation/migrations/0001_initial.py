

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_common', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('invoice_detail_id', models.AutoField(primary_key=True, serialize=False)),
                ('employee_details', models.JSONField(blank=True, default=list, null=True)),
                ('company_name', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('gst_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('esi', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('epf', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('invoice_number', models.CharField(blank=True, max_length=255, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quotation2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('vendor_name', models.CharField(blank=True, max_length=255, null=True)),
                ('post1', models.CharField(blank=True, max_length=255, null=True)),
                ('post2', models.CharField(blank=True, max_length=255, null=True)),
                ('notification_text', models.CharField(blank=True, default='AS PER LABOUR & ESI DEPARTMENT NOTIFICATION DT. 13.03.2024, GoO', max_length=255, null=True)),
                ('semi_skilled', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('unskilled', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('skilled', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('high_skilled', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('semi_skilled_manpower', models.IntegerField(blank=True, null=True)),
                ('unskilled_manpower', models.IntegerField(blank=True, null=True)),
                ('skilled_manpower', models.IntegerField(blank=True, null=True)),
                ('high_skilled_manpower', models.IntegerField(blank=True, null=True)),
                ('working_hours', models.IntegerField(blank=True, null=True)),
                ('working_days', models.IntegerField(blank=True, null=True)),
                ('other_allowances_semi_skilled', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('other_allowances_unskilled', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('other_allowances_skilled', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('other_allowances_high_skilled', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('semi_uniform_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('un_uniform_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('skilled_uniform_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('high_skilled_uniform_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('semi_reliever_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('un_reliever_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('skilled_reliever_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('high_skilled_reliever_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('semi_operational_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('un_operational_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('skilled_operational_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('high_skilled_operational_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('subject', models.CharField(blank=True, max_length=255, null=True)),
                ('to', models.CharField(blank=True, max_length=255, null=True)),
                ('service_charge', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_persons', models.PositiveIntegerField(blank=True, null=True)),
                ('experience_level', models.CharField(blank=True, choices=[('FRESHER', 'FRESHER (Min. 1yr experience)'), ('EXPERIENCED', 'Experienced (Min. 5 yrs)')], max_length=50, null=True)),
                ('salary', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('job_title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_common.job')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component', models.CharField(blank=True, max_length=255, null=True)),
                ('percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('supervisor', models.IntegerField(blank=True, null=True)),
                ('gda', models.IntegerField(blank=True, null=True)),
                ('quotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='quotation.quotation')),
            ],
        ),
    ]
