# Generated by Django 3.2.4 on 2021-06-19 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_data', '0003_auto_20210619_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalaction',
            name='description',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='medicalspeciality',
            name='description',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='service',
            name='details',
            field=models.CharField(max_length=256, verbose_name='Details'),
        ),
        migrations.AlterField(
            model_name='vet',
            name='address',
            field=models.CharField(max_length=128, verbose_name='Address'),
        ),
    ]
