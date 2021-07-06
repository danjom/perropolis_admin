# Generated by Django 3.2.4 on 2021-07-06 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_data', '0011_auto_20210626_0335'),
        ('customers_and_pets', '0006_customer_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Birth Date'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='last_service',
            field=models.DateField(blank=True, null=True, verbose_name='Last Service'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='vet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core_data.vet'),
        ),
    ]