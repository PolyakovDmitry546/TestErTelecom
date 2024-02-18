from django.db import IntegrityError

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from devices.mixins import CustomListModelMixin
from devices.models import Device, DeviceType, TechPlace
from devices.serializers import (
    InDeviceSerializer, InDeviceTypeSerializer, InTechPlaceSerializer,
    InputObjectSerializer, OutDeviceSerializer, OutDeviceTypeSerializer,
    OutTechPlaceSerializer, OutputObjectSerializer
)
from devices.services import CreationService, CreationServiceFactroy


class CreateObjectAPIView(APIView):
    def post(self, request: Request):
        serializer = InputObjectSerializer(data=request.data)
        if serializer.is_valid():
            model = serializer.validated_data.get('__model_type')
            service: CreationService = CreationServiceFactroy.get(model)
            try:
                object_ = service.get_or_create(serializer.data)
            except IntegrityError as e:
                return Response(data=e.args,
                                status=status.HTTP_400_BAD_REQUEST)
            out_serializer = OutputObjectSerializer(object_)
            return Response(data=out_serializer.data,
                            status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CustomListAPIView(CustomListModelMixin, GenericAPIView):
    def get_in_serializer(self):
        return self.input_serializer

    def get_out_serializer(self):
        return self.output_seializer

    def get_model(self):
        return self.model

    def get_queryset(self):
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
