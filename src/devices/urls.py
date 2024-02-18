from django.urls import path

from devices.views import CreateObjectAPIView

urlpatterns = [
    path('object', CreateObjectAPIView.as_view())
]
