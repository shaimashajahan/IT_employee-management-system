# Generated by Django 5.0.6 on 2024-08-20 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0039_alter_module_workprogress_alter_project_workprogress'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='TL',
            field=models.CharField(default=0, max_length=50),
        ),
    ]
