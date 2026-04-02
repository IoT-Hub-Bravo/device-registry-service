import pytest

from apps.registry.api.serializers.device_serializers import (
    DeviceCreateSerializer,
    DeviceUpdateSerializer,
    DeviceOutputSerializer,
)
from apps.registry.api.serializers.metric_serializers import (
    MetricCreateSerializer,
    MetricUpdateSerializer,
)
from apps.registry.tests.factories import DeviceFactory


class TestDeviceCreateSerializer:
    def test_valid_data(self):
        data = {"serial_id": "SN-001", "name": "Sensor", "user_id": 1}
        s = DeviceCreateSerializer(data=data)
        assert s.is_valid()

    def test_missing_required_fields(self):
        s = DeviceCreateSerializer(data={})
        assert not s.is_valid()
        assert "serial_id" in s.errors
        assert "name" in s.errors
        assert "user_id" in s.errors

    def test_invalid_user_id_type(self):
        data = {"serial_id": "SN-001", "name": "Sensor", "user_id": "abc"}
        s = DeviceCreateSerializer(data=data)
        assert not s.is_valid()
        assert "user_id" in s.errors

    def test_optional_fields(self):
        data = {
            "serial_id": "SN-001",
            "name": "Sensor",
            "user_id": 1,
            "description": "A sensor",
            "is_active": False,
        }
        s = DeviceCreateSerializer(data=data)
        assert s.is_valid()
        assert s.validated_data["description"] == "A sensor"
        assert s.validated_data["is_active"] is False


class TestDeviceUpdateSerializer:
    def test_partial_update(self):
        data = {"name": "Updated"}
        s = DeviceUpdateSerializer(data=data)
        assert s.is_valid()
        assert s.validated_data["name"] == "Updated"

    def test_invalid_type(self):
        data = {"is_active": "not_bool"}
        s = DeviceUpdateSerializer(data=data)
        assert not s.is_valid()


@pytest.mark.django_db
class TestDeviceOutputSerializer:
    def test_to_representation(self):
        device = DeviceFactory.create()
        output = DeviceOutputSerializer.to_representation(device)
        assert output["serial_id"] == "SN-TEST-001"
        assert output["name"] == "Test Device"
        assert output["user_id"] == 1
        assert "created_at" in output


class TestMetricCreateSerializer:
    def test_valid_data(self):
        data = {"metric_type": "temperature", "data_type": "numeric"}
        s = MetricCreateSerializer(data=data)
        assert s.is_valid()

    def test_missing_metric_type(self):
        data = {"data_type": "numeric"}
        s = MetricCreateSerializer(data=data)
        assert not s.is_valid()
        assert "metric_type" in s.errors


class TestMetricUpdateSerializer:
    def test_partial_update(self):
        data = {"metric_type": "humidity"}
        s = MetricUpdateSerializer(data=data)
        assert s.is_valid()
        assert s.validated_data["metric_type"] == "humidity"
