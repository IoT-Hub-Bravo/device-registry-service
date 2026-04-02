from django.contrib import admin

from apps.registry.models import Device, Metric, DeviceMetric


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "serial_id", "name", "user_id", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("serial_id", "name")
    readonly_fields = ("created_at",)


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ("id", "metric_type", "data_type")
    search_fields = ("metric_type",)


@admin.register(DeviceMetric)
class DeviceMetricAdmin(admin.ModelAdmin):
    list_display = ("id", "device", "metric")
    list_filter = ("device", "metric")
