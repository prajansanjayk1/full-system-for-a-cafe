from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin

from apps.tenancy.models import Domain


class TenantResolutionMiddleware(MiddlewareMixin):
    """Attach request.tenant from the host name and fail closed for unknown domains."""

    def process_request(self, request):
        host = request.get_host().split(":", 1)[0].lower()
        domain = (
            Domain.objects.select_related("tenant")
            .filter(domain=host, tenant__is_active=True)
            .first()
        )
        if domain is None:
            if host in {"localhost", "127.0.0.1", "testserver"}:
                request.tenant = None
                return None
            raise PermissionDenied("Unknown or inactive tenant domain")
        request.tenant = domain.tenant
        return None
