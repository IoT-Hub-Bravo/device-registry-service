import json
import pytest
from django.test import Client

from apps.registry.tests.factories import DeviceFactory, MetricFactory, DeviceMetricFactory


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
class TestDeviceViews:
    def test_list_devices(self, client):
        DeviceFactory.create(serial_id="SN-1")
        DeviceFactory.create(serial_id="SN-2")
        resp = client.get("/api/devices/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    def test_create_device(self, client):
        resp = client.post(
            "/api/devices/",
            json.dumps({"serial_id": "SN-NEW", "name": "New", "user_id": 1}),
            content_type="application/json",
        )
        assert resp.status_code == 201
        assert resp.json()["serial_id"] == "SN-NEW"

    def test_create_device_duplicate(self, client):
        DeviceFactory.create(serial_id="SN-DUP")
        resp = client.post(
            "/api/devices/",
            json.dumps({"serial_id": "SN-DUP", "name": "Dup", "user_id": 1}),
            content_type="application/json",
        )
        assert resp.status_code == 409

    def test_get_device(self, client):
        device = DeviceFactory.create()
        resp = client.get(f"/api/devices/{device.id}/")
        assert resp.status_code == 200
        assert resp.json()["serial_id"] == device.serial_id

    def test_get_device_not_found(self, client):
        resp = client.get("/api/devices/9999/")
        assert resp.status_code == 404

    def test_update_device_put(self, client):
        device = DeviceFactory.create()
        resp = client.put(
            f"/api/devices/{device.id}/",
            json.dumps({"serial_id": "SN-UPD", "name": "Updated", "user_id": 2}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated"

    def test_update_device_patch(self, client):
        device = DeviceFactory.create()
        resp = client.patch(
            f"/api/devices/{device.id}/",
            json.dumps({"name": "Patched"}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Patched"

    def test_delete_device(self, client):
        device = DeviceFactory.create()
        resp = client.delete(f"/api/devices/{device.id}/")
        assert resp.status_code == 204


@pytest.mark.django_db
class TestMetricViews:
    def test_list_metrics(self, client):
        MetricFactory.create(metric_type="temp")
        resp = client.get("/api/metrics/")
        assert resp.status_code == 200
        assert resp.json()["total"] >= 1

    def test_create_metric(self, client):
        resp = client.post(
            "/api/metrics/",
            json.dumps({"metric_type": "humidity", "data_type": "numeric"}),
            content_type="application/json",
        )
        assert resp.status_code == 201
        assert resp.json()["metric_type"] == "humidity"

    def test_create_metric_duplicate(self, client):
        MetricFactory.create(metric_type="pressure")
        resp = client.post(
            "/api/metrics/",
            json.dumps({"metric_type": "pressure", "data_type": "numeric"}),
            content_type="application/json",
        )
        assert resp.status_code == 409

    def test_delete_metric(self, client):
        metric = MetricFactory.create(metric_type="to_delete")
        resp = client.delete(f"/api/metrics/{metric.id}/")
        assert resp.status_code == 204


@pytest.mark.django_db
class TestDeviceMetricViews:
    def test_bind_metric(self, client):
        device = DeviceFactory.create()
        metric = MetricFactory.create()
        resp = client.post(
            f"/api/devices/{device.id}/metrics/",
            json.dumps({"metric_id": metric.id}),
            content_type="application/json",
        )
        assert resp.status_code == 201

    def test_bind_metric_duplicate(self, client):
        dm = DeviceMetricFactory.create()
        resp = client.post(
            f"/api/devices/{dm.device.id}/metrics/",
            json.dumps({"metric_id": dm.metric.id}),
            content_type="application/json",
        )
        assert resp.status_code == 409

    def test_list_device_metrics(self, client):
        dm = DeviceMetricFactory.create()
        resp = client.get(f"/api/devices/{dm.device.id}/metrics/")
        assert resp.status_code == 200
        assert len(resp.json()["metrics"]) == 1

    def test_unbind_metric(self, client):
        dm = DeviceMetricFactory.create()
        resp = client.delete(f"/api/devices/{dm.device.id}/metrics/{dm.metric.id}/")
        assert resp.status_code == 204


@pytest.mark.django_db
class TestHealthView:
    def test_health_check(self, client):
        resp = client.get("/health/")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"
