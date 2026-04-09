from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.registry.models import Device
from apps.registry.api.serializers import (
    DeviceCreateSerializer,
    DeviceUpdateSerializer,
    DeviceOutputSerializer,
)
from apps.registry.api.utils import parse_json_body
from apps.registry.services.device_service import DeviceService


@method_decorator(csrf_exempt, name="dispatch")
class DeviceView(View):
    def get(self, request):
        try:
            limit = int(request.GET.get("limit", 20))
            offset = int(request.GET.get("offset", 0))
        except ValueError:
            return JsonResponse({"error": "limit and offset must be integers"}, status=400)

        if limit <= 0:
            return JsonResponse({"error": "Limit must be greater than 0"}, status=400)
        if offset < 0:
            return JsonResponse({"error": "Offset must be a positive integer"}, status=400)

        devices_qs = Device.objects.all().order_by("id")
        total = devices_qs.count()
        devices = devices_qs[offset : offset + limit]
        data = [DeviceOutputSerializer.to_representation(d) for d in devices]
        return JsonResponse({"total": total, "limit": limit, "offset": offset, "items": data})

    def post(self, request):
        data, error_response = parse_json_body(request.body)
        if error_response:
            return error_response

        serializer = DeviceCreateSerializer(data)
        if not serializer.is_valid():
            return JsonResponse({"errors": serializer.errors}, status=400)

        try:
            device = DeviceService.create_device(serializer.validated_data)
        except RuntimeError as e:
            return JsonResponse({"error": str(e)}, status=409)

        return JsonResponse(DeviceOutputSerializer.to_representation(device), status=201)


@method_decorator(csrf_exempt, name="dispatch")
class DeviceDetailView(View):
    def get(self, request, pk: int):
        device = get_object_or_404(Device, pk=pk)
        return JsonResponse(DeviceOutputSerializer.to_representation(device))

    def put(self, request, pk: int):
        device = get_object_or_404(Device, pk=pk)
        data, error_response = parse_json_body(request.body)
        if error_response:
            return error_response

        serializer = DeviceCreateSerializer(data)
        if not serializer.is_valid():
            return JsonResponse({"errors": serializer.errors}, status=400)

        try:
            device = DeviceService.update_device(instance=device, data=serializer.validated_data)
        except RuntimeError as e:
            return JsonResponse({"error": str(e)}, status=409)

        return JsonResponse(DeviceOutputSerializer.to_representation(device))

    def patch(self, request, pk: int):
        device = get_object_or_404(Device, pk=pk)
        data, error_response = parse_json_body(request.body)
        if error_response:
            return error_response

        serializer = DeviceUpdateSerializer(data)
        if not serializer.is_valid():
            return JsonResponse({"errors": serializer.errors}, status=400)

        try:
            device = DeviceService.update_device(instance=device, data=serializer.validated_data)
        except RuntimeError as e:
            return JsonResponse({"error": str(e)}, status=409)

        return JsonResponse(DeviceOutputSerializer.to_representation(device))

    def delete(self, request, pk: int):
        device = get_object_or_404(Device, pk=pk)
        DeviceService.delete_device(device)
        return JsonResponse({}, status=204)
