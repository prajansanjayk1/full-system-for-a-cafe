from django.urls import path

from apps.analytics import views

urlpatterns = [path("dashboard/", views.dashboard_view, name="analytics-dashboard")]
