# Generated by Django 5.0.6 on 2024-08-17 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0034_alter_module_workprogress_alter_project_workprogress'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='Epwd',
            field=models.CharField(default=0, max_length=50),
        ),
    ]
