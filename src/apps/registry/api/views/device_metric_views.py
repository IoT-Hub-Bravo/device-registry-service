from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.registry.models import Device, Metric, DeviceMetric
from apps.registry.api.serializers import DeviceMetricOutputSerializer
from apps.registry.api.utils import parse_json_body
from apps.registry.services.kafka_publisher import DeviceEventPublisher


@method_decorator(csrf_exempt, name="dispatch")
class DeviceMetricView(View):
    def get(self, request, device_pk: int):
        device = get_object_or_404(Device, pk=device_pk)
        bindings = DeviceMetric.objects.filter(device=device).select_related("metric")
        data = [DeviceMetricOutputSerializer.to_representation(dm) for dm in bindings]
        return JsonResponse({"device_id": device.id, "metrics": data})

    def post(self, request, device_pk: int):
        device = get_object_or_404(Device, pk=device_pk)
        data, error_response = parse_json_body(request.body)
        if error_response:
            return error_response

        metric_id = data.get("metric_id")
        if not metric_id or not isinstance(metric_id, int):
            return JsonResponse({"error": "metric_id (int) is required"}, status=400)

        metric = get_object_or_404(Metric, pk=metric_id)

        dm, created = DeviceMetric.objects.get_or_create(device=device, metric=metric)
        if not created:
            return JsonResponse(
                {"error": "This metric is already bound to the device"}, status=409
            )

        DeviceEventPublisher.get_instance().device_metric_created(device, metric)
        return JsonResponse(
            DeviceMetricOutputSerializer.to_representation(dm), status=201
        )


@method_decorator(csrf_exempt, name="dispatch")
class DeviceMetricDetailView(View):
    def delete(self, request, device_pk: int, metric_pk: int):
        dm = get_object_or_404(DeviceMetric, device_id=device_pk, metric_id=metric_pk)
        DeviceEventPublisher.get_instance().device_metric_deleted(dm.device, dm.metric)
        dm.delete()
        return JsonResponse({}, status=204)
