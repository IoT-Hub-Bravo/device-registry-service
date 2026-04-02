from django.db import IntegrityError, DatabaseError

from apps.registry.models import Device


class DeviceService:
    @staticmethod
    def create_device(
        *,
        serial_id: str,
        name: str,
        user_id: int,
        description: str | None = None,
        is_active: bool = False,
    ) -> Device:
        try:
            return Device.objects.create(
                serial_id=serial_id,
                name=name,
                description=description,
                user_id=user_id,
                is_active=is_active,
            )
        except IntegrityError:
            raise RuntimeError("Device with the same serial_id already exists")
        except DatabaseError:
            raise RuntimeError("Database error occurred while creating device")

    @staticmethod
    def update_device(*, instance: Device, **kwargs) -> Device:
        for field, value in kwargs.items():
            if value is not None:
                setattr(instance, field, value)
        try:
            instance.save()
            return instance
        except IntegrityError:
            raise RuntimeError("Device update violates a data constraint")
        except DatabaseError:
            raise RuntimeError("Database error occurred while updating device")

    @staticmethod
    def delete_device(device: Device) -> None:
        try:
            device.delete()
        except DatabaseError:
            raise RuntimeError("Database error occurred while deleting device")
