# Generated by Django 5.0.6 on 2024-08-15 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0030_alter_project_workprogress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='workprogress',
            field=models.ImageField(default='static/images/it.jpg', upload_to='image/'),
        ),
    ]