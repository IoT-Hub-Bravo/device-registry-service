from typing import Any

from apps.registry.models import MetricDataType


class MetricCreateSerializer:
    required_fields = ("metric_type",)
    VALID_DATA_TYPES = [choice.value for choice in MetricDataType]

    def __init__(self, data: dict[str, Any] | None = None):
        self.initial_data = data or {}
        self._validated_data = None
        self._errors = None

    def is_valid(self) -> bool:
        self._errors = {}
        self._validated_data = {}

        if not isinstance(self.initial_data, dict):
            self._errors["non_field_errors"] = "Invalid data format"
            return False

        metric_type = self.initial_data.get("metric_type")
        if (
            not metric_type
            or not isinstance(metric_type, str)
            or not metric_type.strip()
        ):
            self._errors["metric_type"] = "This field is required."
            return False
        self._validated_data["metric_type"] = metric_type.strip()

        data_type = self.initial_data.get("data_type", MetricDataType.NUMERIC.value)
        if data_type not in self.VALID_DATA_TYPES:
            self._errors["data_type"] = (
                f"Must be one of: {', '.join(self.VALID_DATA_TYPES)}"
            )
            return False
        self._validated_data["data_type"] = data_type

        return True

    @property
    def validated_data(self):
        if self._validated_data is None:
            raise RuntimeError("Call .is_valid() before accessing .validated_data")
        return self._validated_data

    @property
    def errors(self):
        return self._errors or {}


class MetricUpdateSerializer:
    VALID_DATA_TYPES = [choice.value for choice in MetricDataType]

    def __init__(self, data: dict[str, Any] | None = None):
        self.initial_data = data or {}
        self._validated_data = None
        self._errors = None

    def is_valid(self) -> bool:
        self._errors = {}
        self._validated_data = {}

        if not isinstance(self.initial_data, dict):
            self._errors["non_field_errors"] = "Invalid data format"
            return False

        if "metric_type" in self.initial_data:
            value = self.initial_data["metric_type"]
            if not isinstance(value, str) or not value.strip():
                self._errors["metric_type"] = "Must be a non-empty string."
                return False
            self._validated_data["metric_type"] = value.strip()

        if "data_type" in self.initial_data:
            value = self.initial_data["data_type"]
            if value not in self.VALID_DATA_TYPES:
                self._errors["data_type"] = (
                    f"Must be one of: {', '.join(self.VALID_DATA_TYPES)}"
                )
                return False
            self._validated_data["data_type"] = value

        return True

    @property
    def validated_data(self):
        if self._validated_data is None:
            raise RuntimeError("Call .is_valid() before accessing .validated_data")
        return self._validated_data

    @property
    def errors(self):
        return self._errors or {}


class MetricOutputSerializer:
    @staticmethod
    def to_representation(instance) -> dict[str, Any]:
        return {
            "id": instance.id,
            "metric_type": instance.metric_type,
            "data_type": instance.data_type,
        }
