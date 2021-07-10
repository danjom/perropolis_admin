# Generated by Django 3.2.4 on 2021-07-10 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers_and_pets', '0014_auto_20210710_0624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petimage',
            name='reference_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Reference ID'),
        ),
        migrations.AlterField(
            model_name='petimage',
            name='reference_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Medical Record'), (2, 'Pet Profile'), (3, 'Pet Activity')], null=True, verbose_name='Reference Type'),
        ),
        migrations.AlterField(
            model_name='petvideo',
            name='reference_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Reference ID'),
        ),
        migrations.AlterField(
            model_name='petvideo',
            name='reference_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Medical Record'), (2, 'Pet Profile'), (3, 'Pet Activity')], null=True, verbose_name='Reference Type'),
        ),
    ]
