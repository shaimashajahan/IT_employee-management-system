# Generated by Django 5.0.6 on 2024-08-14 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IT_App', '0020_rename_tl_project_c_user_project_u_member_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='guidelines',
            new_name='file',
        ),
    ]
