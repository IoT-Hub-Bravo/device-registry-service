from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.registry.models import Metric
from apps.registry.api.serializers import (
    MetricCreateSerializer,
    MetricUpdateSerializer,
    MetricOutputSerializer,
)
from apps.registry.api.utils import parse_json_body


@method_decorator(csrf_exempt, name="dispatch")
class MetricView(View):
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

        metrics_qs = Metric.objects.all().order_by("id")
        total = metrics_qs.count()
        metrics = metrics_qs[offset : offset + limit]
        data = [MetricOutputSerializer.to_representation(m) for m in metrics]
        return JsonResponse({"total": total, "limit": limit, "offset": offset, "items": data})

    def post(self, request):
        data, error_response = parse_json_body(request.body)
        if error_response:
            return error_response

        serializer = MetricCreateSerializer(data)
        if not serializer.is_valid():
            return JsonResponse({"errors": serializer.errors}, status=400)

        try:
            metric = Metric.objects.create(**serializer.validated_data)
        except Exception:
            return JsonResponse({"error": "Metric with this type already exists"}, status=409)

        return JsonResponse(MetricOutputSerializer.to_representation(metric), status=201)


@method_decorator(csrf_exempt, name="dispatch")
class MetricDetailView(View):
    def get(self, request, pk: int):
        metric = get_object_or_404(Metric, pk=pk)
        return JsonResponse(MetricOutputSerializer.to_representation(metric))

    def put(self, request, pk: int):
        metric = get_object_or_404(Metric, pk=pk)
        data, error_response = parse_json_body(request.body)
        if error_response:
            return error_response

        serializer = MetricCreateSerializer(data)
        if not serializer.is_valid():
            return JsonResponse({"errors": serializer.errors}, status=400)

        for field, value in serializer.validated_data.items():
            setattr(metric, field, value)

        try:
            metric.save()
        except Exception:
            return JsonResponse({"error": "Metric with this type already exists"}, status=409)

        return JsonResponse(MetricOutputSerializer.to_representation(metric))

    def patch(self, request, pk: int):
        metric = get_object_or_404(Metric, pk=pk)
        data, error_response = parse_json_body(request.body)
        if error_response:
            return error_response

        serializer = MetricUpdateSerializer(data)
        if not serializer.is_valid():
            return JsonResponse({"errors": serializer.errors}, status=400)

        for field, value in serializer.validated_data.items():
            setattr(metric, field, value)

        try:
            metric.save()
        except Exception:
            return JsonResponse({"error": "Metric with this type already exists"}, status=409)

        return JsonResponse(MetricOutputSerializer.to_representation(metric))

    def delete(self, request, pk: int):
        metric = get_object_or_404(Metric, pk=pk)
        metric.delete()
        return JsonResponse({}, status=204)
