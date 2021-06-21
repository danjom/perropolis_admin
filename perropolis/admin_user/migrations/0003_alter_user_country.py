# Generated by Django 3.2.4 on 2021-06-21 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_data', '0006_alter_brand_logo_url'),
        ('admin_user', '0002_auto_20210619_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core_data.country'),
        ),
    ]
