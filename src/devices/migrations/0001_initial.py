# Generated by Django 5.0.2 on 2024-02-17 13:51

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'device_types',
            },
        ),
        migrations.CreateModel(
            name='TechPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
                'db_table': 'tech_places',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created_at', models.DateField(default=datetime.date.today)),
                ('parent_device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='devices.device')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.devicetype')),
                ('tech_place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='devices.techplace')),
            ],
            options={
                'db_table': 'devices',
            },
        ),
    ]