# Generated by Django 5.0.6 on 2024-09-30 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0061_module_desc_project_desc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='crossed_date',
        ),
        migrations.RemoveField(
            model_name='project',
            name='workprogress',
        ),
    ]
