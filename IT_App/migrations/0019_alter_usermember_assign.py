# Generated by Django 5.0.6 on 2024-08-13 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0018_alter_usermember_assign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermember',
            name='assign',
            field=models.CharField(default=1, max_length=50),
        ),
    ]
