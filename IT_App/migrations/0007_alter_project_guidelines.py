# Generated by Django 5.0.6 on 2024-08-10 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0006_rename_certification_usermember_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='guidelines',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]
