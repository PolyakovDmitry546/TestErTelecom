from collections import OrderedDict

from rest_framework import serializers
from devices.mixins import UnknownKeysValidatiorMixin

from devices.models import Device, DeviceType, TechPlace


class InDeviceSerializer(UnknownKeysValidatiorMixin, serializers.Serializer):
    name = serializers.CharField(max_length=200, required=False)
    parent_device_id = serializers.IntegerField(required=False)
    type_id = serializers.IntegerField(required=False)
    created_at = serializers.DateField(required=False)
    tech_place_id = serializers.IntegerField(required=False)


class OutDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
        depth = 1


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class InDeviceTypeSerializer(UnknownKeysValidatiorMixin, serializers.Serializer):
    name = serializers.CharField(max_length=200, required=False)


class OutDeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = '__all__'


class InTechPlaceSerializer(UnknownKeysValidatiorMixin, serializers.Serializer):
    name = serializers.CharField(max_length=200, required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)


class OutTechPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechPlace
        fields = '__all__'


class InputObjectSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    parent_device_id = serializers.IntegerField(
        required=False, allow_null=True)
    type_id = serializers.IntegerField(required=False)
    created_at = serializers.DateField(required=False)
    tech_place_id = serializers.IntegerField(
        required=False, allow_null=True)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)

    object_schemas = {
        frozenset(('name', 'parent_device_id', 'type_id',
                   'created_at', 'tech_place_id')): Device,
        frozenset(('name', 'parent_device_id', 'type_id',
                   'tech_place_id')): Device,
        frozenset(('name', 'latitude', 'longitude')): TechPlace,
        frozenset(('name',)): DeviceType
    }

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        keys = frozenset(validated_data.keys())
        if keys in self.object_schemas:
            validated_data['__model_type'] = self.object_schemas[keys]
        else:
            raise serializers.ValidationError(
                {'error': 'Object of unknown type was passed'})
        return validated_data


class OutputObjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

    def __new__(cls, *args, **kwargs):
        cls.Meta.model = args[0].__class__
        return super().__new__(cls, *args, **kwargs)

    def get_fields(self):
        fields = super().get_fields()
        self.fk_names = set()
        for field in fields.items():
            if isinstance(field[1], serializers.PrimaryKeyRelatedField):
                self.fk_names.add(field[0])
        return fields

    def to_representation(self, instance):
        fields = super().to_representation(instance)
        if not hasattr(self.Meta, 'depth') or self.Meta.depth == 0:
            ret = OrderedDict()
            for key in fields.keys():
                if key in self.fk_names:
                    ret[key+'_id'] = fields[key]
                else:
                    ret[key] = fields[key]
            return ret
        return fields
