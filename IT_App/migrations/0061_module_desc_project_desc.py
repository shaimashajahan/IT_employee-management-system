# Generated by Django 5.0.6 on 2024-09-23 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0060_alter_module_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='desc',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='desc',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
