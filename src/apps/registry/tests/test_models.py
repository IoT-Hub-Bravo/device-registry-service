import pytest
from django.db import IntegrityError

from apps.registry.tests.factories import DeviceFactory, MetricFactory, DeviceMetricFactory


@pytest.mark.django_db
class TestDevice:
    def test_create_device(self):
        device = DeviceFactory.create()
        assert device.id is not None
        assert device.serial_id == "SN-TEST-001"
        assert device.name == "Test Device"
        assert device.user_id == 1
        assert device.is_active is True
        assert device.created_at is not None

    def test_serial_id_unique(self):
        DeviceFactory.create(serial_id="SN-UNIQUE")
        with pytest.raises(IntegrityError):
            DeviceFactory.create(serial_id="SN-UNIQUE")

    def test_description_nullable(self):
        device = DeviceFactory.create(description=None)
        assert device.description is None

    def test_str_representation(self):
        device = DeviceFactory.create(name="My Sensor")
        assert str(device.id) in str(device.id)


@pytest.mark.django_db
class TestMetric:
    def test_create_metric(self):
        metric = MetricFactory.create()
        assert metric.id is not None
        assert metric.metric_type == "temperature"
        assert metric.data_type == "numeric"

    def test_metric_type_unique(self):
        MetricFactory.create(metric_type="humidity")
        with pytest.raises(IntegrityError):
            MetricFactory.create(metric_type="humidity")

    def test_data_type_choices(self):
        m1 = MetricFactory.create(metric_type="t1", data_type="numeric")
        m2 = MetricFactory.create(metric_type="t2", data_type="bool")
        m3 = MetricFactory.create(metric_type="t3", data_type="str")
        assert m1.data_type == "numeric"
        assert m2.data_type == "bool"
        assert m3.data_type == "str"


@pytest.mark.django_db
class TestDeviceMetric:
    def test_create_device_metric(self):
        dm = DeviceMetricFactory.create()
        assert dm.id is not None
        assert dm.device is not None
        assert dm.metric is not None

    def test_unique_together(self):
        device = DeviceFactory.create()
        metric = MetricFactory.create()
        DeviceMetricFactory.create(device=device, metric=metric)
        with pytest.raises(IntegrityError):
            DeviceMetricFactory.create(device=device, metric=metric)

    def test_cascade_delete_device(self):
        dm = DeviceMetricFactory.create()
        device_id = dm.device.id
        dm.device.delete()
        from apps.registry.models import DeviceMetric
        assert not DeviceMetric.objects.filter(device_id=device_id).exists()

    def test_restrict_delete_metric(self):
        dm = DeviceMetricFactory.create()
        from django.db.models import RestrictedError
        with pytest.raises(RestrictedError):
            dm.metric.delete()
