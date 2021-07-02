# Generated by Django 3.2.4 on 2021-06-26 10:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_data', '0011_auto_20210626_0335'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business_locations', '0004_auto_20210626_0335'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_location_services', to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='business_locations.location')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core_data.service')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='updated_location_services', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Location Service',
                'verbose_name_plural': 'Location Services',
                'db_table': 'location_services',
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_zones', to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='business_locations.location')),
                ('location_service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='business_locations.locationservice')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core_data.service')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='updated_zones', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Zone',
                'verbose_name_plural': 'Zones',
                'db_table': 'zones',
            },
        ),
        migrations.CreateModel(
            name='Webcam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(max_length=64, verbose_name='External ID')),
                ('code', models.CharField(max_length=20, verbose_name='Code')),
                ('alias', models.CharField(max_length=30, unique=True, verbose_name='Alias')),
                ('web_url', models.CharField(blank=True, max_length=128, null=True, verbose_name='Web URL')),
                ('app_url', models.CharField(blank=True, max_length=128, null=True, verbose_name='APP URL')),
                ('livestream_available', models.BooleanField(default=False, verbose_name='Livestream Available')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_webcams', to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='business_locations.location')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='updated_webcams', to=settings.AUTH_USER_MODEL)),
                ('zone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='business_locations.zone')),
            ],
            options={
                'verbose_name': 'Webcam',
                'verbose_name_plural': 'Webcams',
                'db_table': 'webcams',
            },
        ),
        migrations.CreateModel(
            name='ServiceCapacity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.IntegerField(choices=[(1, 'Food'), (2, 'Medication')], verbose_name='Service Type')),
                ('max_capacity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_service_capacities', to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='business_locations.location')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='updated_service_capacities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Service Capacity',
                'verbose_name_plural': 'Service Capacities',
                'db_table': 'service_capacities',
            },
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_size', models.IntegerField(choices=[(1, 'Small'), (2, 'Medium'), (3, 'Large')], verbose_name='Pet Size')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Price')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_pricings', to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='business_locations.location')),
                ('location_service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='business_locations.locationservice')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core_data.service')),
                ('specie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core_data.specie')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='updated_pricings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pricing',
                'verbose_name_plural': 'Pricings',
                'db_table': 'pricing',
            },
        ),
        migrations.AddIndex(
            model_name='zone',
            index=models.Index(fields=['location_id', 'name'], name='ix_zone_name'),
        ),
        migrations.AlterUniqueTogether(
            name='zone',
            unique_together={('location_id', 'name')},
        ),
        migrations.AddIndex(
            model_name='webcam',
            index=models.Index(fields=['alias'], name='ix_webcam_alias'),
        ),
        migrations.AddIndex(
            model_name='servicecapacity',
            index=models.Index(fields=['location_id', 'service_type'], name='ix_service_capacity'),
        ),
        migrations.AddIndex(
            model_name='servicecapacity',
            index=models.Index(fields=['service_type'], name='ix_service_type'),
        ),
        migrations.AlterUniqueTogether(
            name='servicecapacity',
            unique_together={('location_id', 'service_type')},
        ),
        migrations.AddIndex(
            model_name='pricing',
            index=models.Index(fields=['service_id', 'location_id'], name='ix_pricing_service_location'),
        ),
        migrations.AlterUniqueTogether(
            name='pricing',
            unique_together={('service_id', 'location_id')},
        ),
        migrations.AddIndex(
            model_name='locationservice',
            index=models.Index(fields=['service_id', 'location_id'], name='ix_service_location'),
        ),
        migrations.AlterUniqueTogether(
            name='locationservice',
            unique_together={('service_id', 'location_id')},
        ),
    ]