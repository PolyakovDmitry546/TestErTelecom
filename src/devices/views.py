from django.db import IntegrityError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from devices.serializers import InputObjectSerializer, OutputObjectSerializer
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
