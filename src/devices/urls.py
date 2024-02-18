from django.urls import path

from devices.views import (
    CreateObjectAPIView, DeviceListAPIView, DeviceTypeListAPIView,
    DeviceTypeUpdateAPIView, DeviceUpdateAPIView, TechPlaceListAPIView,
    TechPlaceUpdateAPIView
)


urlpatterns = [
    path('object', CreateObjectAPIView.as_view()),
    path('device/<int:pk>', DeviceUpdateAPIView.as_view()),
    path('device', DeviceListAPIView.as_view()),
    path('device-type/<int:pk>', DeviceTypeUpdateAPIView.as_view()),
    path('device-type', DeviceTypeListAPIView.as_view()),
    path('tech-place/<int:pk>', TechPlaceUpdateAPIView.as_view()),
    path('tech-place', TechPlaceListAPIView.as_view()),
]
