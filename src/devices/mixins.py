from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


class CustomListModelMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if len(queryset) == 0:
            return Response({})
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_out_serializer()(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_out_serializer()(queryset, many=True)
        return Response(serializer.data)


class UnknownKeysValidatiorMixin:
    def validate(self, attr):
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                raise ValidationError("Got unknown fields: {}".format(unknown_keys))
        return super().validate(attr)
