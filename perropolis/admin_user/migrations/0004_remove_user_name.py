# Generated by Django 3.2.4 on 2021-06-22 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0003_alter_user_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
    ]
