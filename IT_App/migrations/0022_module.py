# Generated by Django 5.0.6 on 2024-08-14 11:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0021_rename_guidelines_project_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_name', models.CharField(max_length=255, null=True)),
                ('file', models.FileField(upload_to='uploads/')),
                ('u_member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='IT_App.usermember')),
            ],
        ),
    ]