from typing import Any, Optional

from iot_hub_shared.serializer_kit import JSONSerializer
from apps.registry.models import MetricDataType


class MetricCreateSerializer(JSONSerializer):
    REQUIRED_FIELDS = {
        "metric_type": str,
    }
    OPTIONAL_FIELDS = {
        "data_type": str,
    }

    VALID_DATA_TYPES = [choice.value for choice in MetricDataType]

    def _validate_fields(self, data: dict[str, Any]) -> Optional[dict[str, Any]]:
        metric_type = data["metric_type"].strip()
        if not metric_type:
            self._errors["metric_type"] = "metric_type must be a non-empty string."
            return None

        data_type = data.get("data_type", MetricDataType.NUMERIC.value)
        if data_type not in self.VALID_DATA_TYPES:
            self._errors["data_type"] = f"Must be one of: {', '.join(self.VALID_DATA_TYPES)}"
            return None

        return {
            "metric_type": metric_type,
            "data_type": data_type,
        }


class MetricUpdateSerializer(JSONSerializer):
    REQUIRED_FIELDS = {}
    OPTIONAL_FIELDS = {
        "metric_type": str,
        "data_type": str,
    }
    STRICT_SCHEMA = True

    VALID_DATA_TYPES = [choice.value for choice in MetricDataType]

    def _validate_fields(self, data: dict[str, Any]) -> Optional[dict[str, Any]]:
        validated = {}

        if "metric_type" in data:
            metric_type = data["metric_type"].strip()
            if not metric_type:
                self._errors["metric_type"] = "Must be a non-empty string."
                return None
            validated["metric_type"] = metric_type

        if "data_type" in data:
            if data["data_type"] not in self.VALID_DATA_TYPES:
                self._errors["data_type"] = f"Must be one of: {', '.join(self.VALID_DATA_TYPES)}"
                return None
            validated["data_type"] = data["data_type"]

        return validated


class MetricOutputSerializer:
    @staticmethod
    def to_representation(instance) -> dict[str, Any]:
        return {
            "id": instance.id,
            "metric_type": instance.metric_type,
            "data_type": instance.data_type,
        }
