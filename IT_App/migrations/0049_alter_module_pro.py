# Generated by Django 5.0.6 on 2024-09-03 05:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0048_remove_module_tl_remove_module_connect_dev_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='pro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='IT_App.project_tl'),
        ),
    ]
