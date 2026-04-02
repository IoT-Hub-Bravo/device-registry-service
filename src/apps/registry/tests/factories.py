from apps.registry.models import Device, Metric, DeviceMetric


class DeviceFactory:
    @staticmethod
    def create(**kwargs):
        defaults = {
            "serial_id": "SN-TEST-001",
            "name": "Test Device",
            "user_id": 1,
            "is_active": True,
        }
        defaults.update(kwargs)
        return Device.objects.create(**defaults)


class MetricFactory:
    @staticmethod
    def create(**kwargs):
        defaults = {
            "metric_type": "temperature",
            "data_type": "numeric",
        }
        defaults.update(kwargs)
        return Metric.objects.create(**defaults)


class DeviceMetricFactory:
    @staticmethod
    def create(**kwargs):
        device = kwargs.pop("device", None) or DeviceFactory.create()
        metric = kwargs.pop("metric", None) or MetricFactory.create()
        return DeviceMetric.objects.create(device=device, metric=metric, **kwargs)
