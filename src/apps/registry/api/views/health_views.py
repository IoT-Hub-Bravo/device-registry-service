from django.db import connection
from django.http import JsonResponse


def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "healthy", "database": "ok"})
    except Exception as e:
        return JsonResponse(
            {"status": "unhealthy", "database": str(e)}, status=503
        )