from django.urls import path

from .views import (
    DeviceView,
    DeviceDetailView,
    MetricView,
    MetricDetailView,
    DeviceMetricView,
    DeviceMetricDetailView,
)

urlpatterns = [
    path("devices/", DeviceView.as_view(), name="device-list-create"),
    path("devices/<int:pk>/", DeviceDetailView.as_view(), name="device-detail"),
    path("metrics/", MetricView.as_view(), name="metric-list-create"),
    path("metrics/<int:pk>/", MetricDetailView.as_view(), name="metric-detail"),
    path(
        "devices/<int:device_pk>/metrics/",
        DeviceMetricView.as_view(),
        name="device-metric-list-bind",
    ),
    path(
        "devices/<int:device_pk>/metrics/<int:metric_pk>/",
        DeviceMetricDetailView.as_view(),
        name="device-metric-unbind",
    ),
]
