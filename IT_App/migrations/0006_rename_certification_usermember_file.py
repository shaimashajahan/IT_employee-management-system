# Generated by Django 5.0.6 on 2024-08-10 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0005_usermember_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermember',
            old_name='certification',
            new_name='file',
        ),
    ]
