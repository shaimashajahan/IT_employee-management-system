# Generated by Django 5.0.6 on 2024-09-04 05:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0050_module_dev'),
    ]

    operations = [
        migrations.CreateModel(
            name='teamlead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dev', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='IT_App.usermember')),
            ],
        ),
    ]