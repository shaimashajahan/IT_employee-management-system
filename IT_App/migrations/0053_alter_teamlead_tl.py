# Generated by Django 5.0.6 on 2024-09-04 05:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0052_rename_dev_teamlead_tl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamlead',
            name='tl',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
