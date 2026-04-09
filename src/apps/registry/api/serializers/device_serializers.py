from typing import Any, Optional

from iot_hub_shared.serializer_kit import JSONSerializer


class DeviceCreateSerializer(JSONSerializer):
    REQUIRED_FIELDS = {
        "serial_id": str,
        "name": str,
        "user_id": int,
    }
    OPTIONAL_FIELDS = {
        "description": (str, type(None)),
        "is_active": bool,
    }

    def _validate_fields(self, data: dict[str, Any]) -> Optional[dict[str, Any]]:
        serial_id = data["serial_id"].strip()
        name = data["name"].strip()

        if not serial_id:
            self._errors["serial_id"] = "serial_id must be a non-empty string."
        if not name:
            self._errors["name"] = "name must be a non-empty string."

        if self._errors:
            return None

        return {
            "serial_id": serial_id,
            "name": name,
            "user_id": data["user_id"],
            "description": data.get("description"),
            "is_active": data.get("is_active", True),
        }


class DeviceUpdateSerializer(JSONSerializer):
    REQUIRED_FIELDS = {}
    OPTIONAL_FIELDS = {
        "name": str,
        "description": (str, type(None)),
        "is_active": bool,
    }
    STRICT_SCHEMA = True

    def _validate_fields(self, data: dict[str, Any]) -> Optional[dict[str, Any]]:
        validated = {}

        if "name" in data:
            name = data["name"].strip()
            if not name:
                self._errors["name"] = "name must be a non-empty string."
                return None
            validated["name"] = name

        if "description" in data:
            validated["description"] = data["description"]

        if "is_active" in data:
            validated["is_active"] = data["is_active"]

        return validated


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
