from django.contrib import admin
from django.urls import include, path

from apps.core.views import healthz

urlpatterns = [
    # Lightweight endpoint used by Docker, Nginx, and local smoke checks.
    path("healthz/", healthz, name="healthz"),
=======
urlpatterns = [
    path("admin/", admin.site.urls),
    path("orders/", include("apps.orders.urls")),
    path("payments/", include("apps.payments.urls")),
    path("kitchen/", include("apps.kitchen.urls")),
    path("analytics/", include("apps.analytics.urls")),
]
