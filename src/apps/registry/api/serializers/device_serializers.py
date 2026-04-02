from typing import Any


class DeviceCreateSerializer:
    required_fields = ("serial_id", "name", "user_id")
    FIELD_TYPES = {
        "serial_id": str,
        "name": str,
        "description": (str, type(None)),
        "user_id": int,
        "is_active": bool,
    }

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

        for field in self.required_fields:
            if field not in self.initial_data or self.initial_data[field] in ("", None):
                self._errors[field] = "This field is required."

        if self._errors:
            return False

        for field, expected_type in self.FIELD_TYPES.items():
            if field in self.initial_data:
                value = self.initial_data[field]
                if not isinstance(value, expected_type):
                    self._errors[field] = f"'{field}' must be a valid value."
                elif isinstance(value, str):
                    self._validated_data[field] = value.strip()
                else:
                    self._validated_data[field] = value

        return not bool(self._errors)

    @property
    def validated_data(self):
        if self._validated_data is None:
            raise RuntimeError("Call .is_valid() before accessing .validated_data")
        return self._validated_data

    @property
    def errors(self):
        return self._errors or {}


class DeviceUpdateSerializer:
    FIELD_TYPES = {
        "name": str,
        "description": (str, type(None)),
        "is_active": bool,
    }

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

        for field, expected_type in self.FIELD_TYPES.items():
            if field in self.initial_data:
                value = self.initial_data[field]
                if not isinstance(value, expected_type):
                    self._errors[field] = f"'{field}' must be a valid value."
                elif isinstance(value, str):
                    self._validated_data[field] = value.strip()
                else:
                    self._validated_data[field] = value

        return not bool(self._errors)

    @property
    def validated_data(self):
        if self._validated_data is None:
            raise RuntimeError("Call .is_valid() before accessing .validated_data")
        return self._validated_data

    @property
    def errors(self):
        return self._errors or {}


class DeviceOutputSerializer:
    @staticmethod
    def to_representation(instance) -> dict[str, Any]:
        return {
            "id": instance.id,
            "serial_id": instance.serial_id,
            "name": instance.name,
            "description": instance.description,
            "user_id": instance.user_id,
            "is_active": instance.is_active,
            "created_at": (
                instance.created_at.isoformat() if instance.created_at else None
            ),
        }
