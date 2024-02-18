from django.urls import path

from devices.views import (
    CreateObjectAPIView, DeviceListAPIView, DeviceTypeListAPIView,
    TechPlaceListAPIView
)


urlpatterns = [
    path('object', CreateObjectAPIView.as_view()),
    path('device', DeviceListAPIView.as_view()),
    path('device-type', DeviceTypeListAPIView.as_view()),
    path('tech-place', TechPlaceListAPIView.as_view()),
]
