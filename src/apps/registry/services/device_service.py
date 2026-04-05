from typing import TypedDict, Optional

from django.db import IntegrityError

from apps.registry.models import Device
from apps.registry.services.kafka_publisher import DeviceEventPublisher


class DeviceCreateData(TypedDict):
    serial_id: str
    name: str
    user_id: int
    description: Optional[str]
    is_active: bool


class DeviceUpdateData(TypedDict, total=False):
    name: Optional[str]
    description: Optional[str]
    is_active: Optional[bool]


class DeviceService:
    @staticmethod
    def create_device(data: DeviceCreateData) -> Device:
        try:
            device = Device.objects.create(**data)
        except IntegrityError:
            raise RuntimeError("Device with the same serial_id already exists")
        DeviceEventPublisher.get_instance().device_created(device)
        return device

    @staticmethod
    def update_device(instance: Device, data: DeviceUpdateData) -> Device:
        for key, value in data.items():
            if value is not None:
                setattr(instance, key, value)
        try:
            instance.save()
        except IntegrityError:
            raise RuntimeError("Device with the same serial_id already exists")
        DeviceEventPublisher.get_instance().device_updated(instance)
        return instance

    @staticmethod
    def delete_device(instance: Device) -> None:
        serial_id = instance.serial_id
        instance.delete()
        DeviceEventPublisher.get_instance().device_deleted(serial_id)
