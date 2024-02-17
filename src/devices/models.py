from datetime import date

from django.db import models


class Device(models.Model):
    parent_device = models.ForeignKey('self', on_delete=models.SET_NULL,
                                      null=True)
    name = models.CharField(max_length=200)
    type = models.ForeignKey('DeviceType', on_delete=models.CASCADE)
    created_at = models.DateField(default=date.today)
    tech_place = models.ForeignKey('TechPlace', on_delete=models.SET_NULL,
                                   null=True)

    class Meta:
        db_table = 'devices'


class DeviceType(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'device_types'


class TechPlace(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = 'tech_places'
