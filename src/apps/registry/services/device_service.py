from apps.registry.models import Device
from apps.registry.services.kafka_publisher import DeviceEventPublisher


class DeviceService:
    @staticmethod
    def create_device(**data) -> Device:
        device = Device.objects.create(**data)
        DeviceEventPublisher.get_instance().device_created(device)
        return device

    @staticmethod
    def update_device(instance: Device, **data) -> Device:
        for key, value in data.items():
            if value is not None:
                setattr(instance, key, value)
        instance.save()
        DeviceEventPublisher.get_instance().device_updated(instance)
        return instance

    @staticmethod
    def delete_device(instance: Device) -> None:
        serial_id = instance.serial_id
        instance.delete()
        DeviceEventPublisher.get_instance().device_deleted(serial_id)
