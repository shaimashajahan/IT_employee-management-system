# Generated by Django 5.0.6 on 2024-08-11 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0008_remove_usermember_status_customuser_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='status',
            field=models.CharField(max_length=50),
        ),
    ]
