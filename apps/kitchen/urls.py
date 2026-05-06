from django.urls import path

from apps.kitchen import views

urlpatterns = [
    path("tickets/", views.ticket_feed_view, name="kitchen-ticket-feed"),
    path("tickets/<uuid:ticket_id>/status/", views.ticket_status_view, name="kitchen-ticket-status"),
]
