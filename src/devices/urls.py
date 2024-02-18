from django.urls import path

from devices.views import (
    CreateObjectAPIView, DeviceCSVView, DeviceListAPIView,
    DeviceTypeCSVView, DeviceTypeListAPIView, DeviceTypeUpdateAPIView,
    DeviceUpdateAPIView, TechPlaceCSVView, TechPlaceListAPIView,
    TechPlaceUpdateAPIView
)


urlpatterns = [
    path('object', CreateObjectAPIView.as_view()),
    path('device/<int:pk>/csv', DeviceCSVView.as_view()),
    path('device/<int:pk>', DeviceUpdateAPIView.as_view()),
    path('device', DeviceListAPIView.as_view()),
    path('device-type/<int:pk>/csv', DeviceTypeCSVView.as_view()),
    path('device-type/<int:pk>', DeviceTypeUpdateAPIView.as_view()),
    path('device-type', DeviceTypeListAPIView.as_view()),
    path('tech-place/<int:pk>/csv', TechPlaceCSVView.as_view()),
    path('tech-place/<int:pk>', TechPlaceUpdateAPIView.as_view()),
    path('tech-place', TechPlaceListAPIView.as_view()),
]
