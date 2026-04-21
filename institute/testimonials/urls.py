from django.urls import path
from .views import TestimonialListView

app_name = 'testimonials'

urlpatterns = [
    path('', TestimonialListView.as_view(), name='testimonial_list'),
]
