from django.db import IntegrityError

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin

from devices.mixins import CustomListModelMixin
from devices.models import Device, DeviceType, TechPlace
from devices.serializers import (
    DeviceSerializer, InDeviceSerializer, InDeviceTypeSerializer,
    InTechPlaceSerializer, InputObjectSerializer, OutDeviceSerializer,
    OutDeviceTypeSerializer, OutTechPlaceSerializer, OutputObjectSerializer
)
from devices.services import CreationService


class CreateObjectAPIView(APIView):
    """Содержит реализацию POST запроса который:
        принимает на вход JSON объект. Если найден объект с идентичным
        содержимым, возвращает сериализованный объект из базы (с его id),
        иначе добавляет объект в базу и так же возвращает созданный объект.
    """
    def post(self, request: Request):
        serializer = InputObjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        model = serializer.validated_data.pop('__model_type')
        service = CreationService(model)
        try:
            object_ = service.get_or_create(serializer.validated_data)
        except IntegrityError as e:
            return Response(data=e.args,
                            status=status.HTTP_400_BAD_REQUEST)
        out_serializer = OutputObjectSerializer(object_)
        return Response(data=out_serializer.data,
                        status=status.HTTP_200_OK)


class CustomListAPIView(CustomListModelMixin, GenericAPIView):
    """Содержит реализацию GET запроса который:
        принимает на вход JSON объект (не обязательно). Если найдено
        совпадение по переданным полям, то выводит сериализованный объект.
        Ecли совпаденией не найденно возвращает пустой объект.
        Если не передано ничего, выводит список всех объектов модели.
    """
    def get_in_serializer(self):
        return self.input_serializer

    def get_out_serializer(self):
        return self.output_seializer

    def get_model(self):
        return self.model

    def get_queryset(self):
        """Если запрос не содержит даннх, возвращет все объекты модели.
        """
        if not self.request.data:
            return self.get_model().objects.all()
        serializer = self.get_in_serializer()(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        queryset = self.get_model().objects.filter(**serializer.data)
        return queryset

    def get(self, request, *args, **kwargs):
        self.request = request
        return self.list(request, *args, **kwargs)


class DeviceListAPIView(CustomListAPIView):
    input_serializer = InDeviceSerializer
    output_seializer = OutDeviceSerializer
    model = Device


class DeviceTypeListAPIView(CustomListAPIView):
    input_serializer = InDeviceTypeSerializer
    output_seializer = OutDeviceTypeSerializer
    model = DeviceType


class TechPlaceListAPIView(CustomListAPIView):
    input_serializer = InTechPlaceSerializer
    output_seializer = OutTechPlaceSerializer
    model = TechPlace


class CustomUpdateView(UpdateModelMixin, GenericAPIView):
    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DeviceUpdateAPIView(CustomUpdateView):
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()


class DeviceTypeUpdateAPIView(CustomUpdateView):
    serializer_class = OutDeviceTypeSerializer
    queryset = DeviceType.objects.all()


class TechPlaceUpdateAPIView(CustomUpdateView):
    serializer_class = OutTechPlaceSerializer
    queryset = TechPlace.objects.all()
