# Generated by Django 5.0.6 on 2024-08-24 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0040_customuser_tl'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='TL',
            field=models.CharField(default=0, max_length=50),
        ),
    ]
