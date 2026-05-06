from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("orders/", include("apps.orders.urls")),
    path("payments/", include("apps.payments.urls")),
    path("kitchen/", include("apps.kitchen.urls")),
    path("analytics/", include("apps.analytics.urls")),
]
