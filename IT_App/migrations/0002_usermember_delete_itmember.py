# Generated by Django 5.0.6 on 2024-08-07 06:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usermember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, null=True)),
                ('number', models.CharField(max_length=255, null=True)),
                ('course', models.CharField(max_length=255, null=True)),
                ('certification', models.FileField(upload_to='uploads/')),
                ('department', models.CharField(max_length=255, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='ITmember',
        ),
    ]