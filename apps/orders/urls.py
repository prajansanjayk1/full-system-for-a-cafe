from django.urls import path

from apps.orders import views

urlpatterns = [
    path("", views.create_order_view, name="orders-create"),
    path("<uuid:order_id>/", views.order_detail_view, name="orders-detail"),
    path("<uuid:order_id>/transition/", views.transition_order_view, name="orders-transition"),
]
