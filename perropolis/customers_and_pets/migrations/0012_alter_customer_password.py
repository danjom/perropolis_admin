# Generated by Django 3.2.4 on 2021-07-07 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers_and_pets', '0011_auto_20210706_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
