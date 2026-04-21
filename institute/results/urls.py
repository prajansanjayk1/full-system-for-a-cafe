from django.urls import path
from .views import ResultListView

app_name = 'results'

urlpatterns = [
    path('', ResultListView.as_view(), name='result_list'),
]
