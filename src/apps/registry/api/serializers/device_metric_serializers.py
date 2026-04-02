from typing import Any


class DeviceMetricOutputSerializer:
    @staticmethod
    def to_representation(instance) -> dict[str, Any]:
        return {
            "id": instance.id,
            "device_id": instance.device_id,
            "metric_id": instance.metric_id,
            "metric_type": instance.metric.metric_type,
            "data_type": instance.metric.data_type,
        }
