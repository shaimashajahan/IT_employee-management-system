# Generated by Django 5.0.6 on 2024-08-13 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0016_assigntl_assign'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='assign',
        ),
        migrations.AddField(
            model_name='usermember',
            name='assign',
            field=models.CharField(default=1, max_length=50),
        ),
        migrations.DeleteModel(
            name='assignTL',
        ),
    ]
