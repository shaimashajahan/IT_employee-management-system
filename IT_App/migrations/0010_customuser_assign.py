# Generated by Django 5.0.6 on 2024-08-12 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0009_alter_customuser_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='assign',
            field=models.CharField(default=1, max_length=50),
        ),
    ]
