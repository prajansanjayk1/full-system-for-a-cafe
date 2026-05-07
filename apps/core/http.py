import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


def json_body(request):
    if not request.body:
        return {}
    return json.loads(request.body.decode("utf-8"))


def tenant_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.tenant is None:
            return JsonResponse({"error": "tenant_required"}, status=400)
        return view_func(request, *args, **kwargs)

    return wrapper
