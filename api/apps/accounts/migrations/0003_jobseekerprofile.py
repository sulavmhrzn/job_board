# Generated by Django 5.1.6 on 2025-02-25 07:12

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_date_joined'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobSeekerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('gender', models.TextField(choices=[('MALE', 'Male'), ('FEMALE', 'FEMALE'), ('OTHERS', 'Others')], max_length=20)),
                ('date_of_birth', models.DateField(blank=True)),
                ('current_address', models.CharField()),
                ('permanent_address', models.CharField()),
                ('marital_status', models.CharField(choices=[('UNMARRIED', 'Unmarried'), ('MARRIED', 'MARRIED')], max_length=20)),
                ('resume', models.FileField(blank=True, upload_to='resumes/')),
                ('profile_picture', models.ImageField(blank=True, upload_to='profile_pictures/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='job_seeker_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
