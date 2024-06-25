# Generated by Django 4.2 on 2024-06-21 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_common', '0008_alter_userprofile_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='category',
            new_name='catagory',
        ),
        migrations.AddField(
            model_name='job',
            name='company_logo',
            field=models.ImageField(blank=True, null=True, upload_to='company_logos/'),
        ),
        migrations.AddField(
            model_name='job',
            name='company_name',
            field=models.CharField(default='Default Company', max_length=255),
        ),
        migrations.AddField(
            model_name='job',
            name='company_website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='job',
            name='publish_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='job',
            name='vacancies',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
