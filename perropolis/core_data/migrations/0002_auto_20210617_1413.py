# Generated by Django 3.2.4 on 2021-06-17 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='brand_type',
            field=models.IntegerField(choices=[(1, 'Food/Snacks'), (2, 'Drugs'), (3, 'Accesories/Toys')], verbose_name='Brand Type'),
        ),
        migrations.AlterField(
            model_name='breed',
            name='size',
            field=models.IntegerField(choices=[(1, 'Tea cup'), (2, 'Small'), (3, 'Medium'), (4, 'Large'), (5, 'GIANT')]),
        ),
        migrations.AlterField(
            model_name='medicalspeciality',
            name='description',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='petdrug',
            name='drug_type',
            field=models.IntegerField(choices=[(1, 'Pills'), (2, 'Inyection'), (3, 'Syrup'), (4, 'Suppository')], verbose_name='Drug Type'),
        ),
    ]