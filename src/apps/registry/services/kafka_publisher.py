import uuid
import logging
from datetime import datetime, timezone
from typing import Any

from iot_hub_shared.kafka_kit import KafkaProducer, ProducerConfig, ProduceResult

logger = logging.getLogger(__name__)

TOPIC = "device.registry"
SOURCE = "device-registry-service"


def _build_headers(
    event_type: str, version: str = "v1", correlation_id: str | None = None
) -> dict:
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "version": version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": SOURCE,
        "correlation_id": correlation_id or str(uuid.uuid4()),
    }


class DeviceEventPublisher:
    _instance: "DeviceEventPublisher | None" = None
    _producer: KafkaProducer | None = None

    @classmethod
    def get_instance(cls) -> "DeviceEventPublisher":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        try:
            config = ProducerConfig()
            self._producer = KafkaProducer(config=config, topic=TOPIC)
        except Exception:
            logger.exception("Failed to initialize KafkaProducer")
            self._producer = None

    def _publish(self, event_type: str, payload: dict[str, Any], key: str | None = None) -> bool:
        if self._producer is None:
            logger.warning("KafkaProducer not available, skipping event: %s", event_type)
            return False

        message = {
            "headers": _build_headers(event_type),
            "payload": payload,
        }

        result = self._producer.produce(payload=message, key=key)
        if result == ProduceResult.ENQUEUED:
            logger.info("Event published: %s", event_type)
            return True
        else:
            logger.warning("Failed to publish event: %s, result: %s", event_type, result)
            return False

    def device_created(self, device) -> bool:
        from apps.registry.models import DeviceMetric

        metrics = DeviceMetric.objects.filter(device=device).select_related("metric")
        payload = {
            "device_serial_id": device.serial_id,
            "metrics": [
                {
                    "name": dm.metric.metric_type,
                    "type": dm.metric.data_type,
                }
                for dm in metrics
            ],
            "created_at": device.created_at.isoformat(),
        }
        return self._publish("device.created.v1", payload, key=device.serial_id)

    def device_updated(self, device) -> bool:
        payload = {
            "device_serial_id": device.serial_id,
            "name": device.name,
            "description": device.description,
            "is_active": device.is_active,
            "user_id": device.user_id,
        }
        return self._publish("device.updated.v1", payload, key=device.serial_id)

    def device_deleted(self, device_serial_id: str) -> bool:
        payload = {
            "device_serial_id": device_serial_id,
        }
        return self._publish("device.deleted.v1", payload, key=device_serial_id)

    def device_metric_created(self, device, metric) -> bool:
        payload = {
            "device_serial_id": device.serial_id,
            "metric_name": metric.metric_type,
            "metric_type": metric.data_type,
        }
        return self._publish("device_metric.created.v1", payload, key=device.serial_id)

    def device_metric_deleted(self, device, metric) -> bool:
        payload = {
            "device_serial_id": device.serial_id,
            "metric_name": metric.metric_type,
        }
        return self._publish("device_metric.deleted.v1", payload, key=device.serial_id)

    def shutdown(self):
        if self._producer:
            self._producer.flush()
