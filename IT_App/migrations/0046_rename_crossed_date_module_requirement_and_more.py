# Generated by Django 5.0.6 on 2024-09-02 18:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0045_alter_module_tl'),
    ]

    operations = [
        migrations.RenameField(
            model_name='module',
            old_name='crossed_date',
            new_name='requirement',
        ),
        migrations.RemoveField(
            model_name='module',
            name='TL',
        ),
        migrations.RemoveField(
            model_name='module',
            name='connect_dev',
        ),
        migrations.RemoveField(
            model_name='module',
            name='workprogress',
        ),
        migrations.AddField(
            model_name='module',
            name='pro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='IT_App.project'),
        ),
    ]