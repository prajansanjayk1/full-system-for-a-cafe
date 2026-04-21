from django.urls import path
from .views import SubjectListView, SubjectDetailView

app_name = 'subjects'

urlpatterns = [
    path('', SubjectListView.as_view(), name='subject_list'),
    path('<slug:slug>/', SubjectDetailView.as_view(), name='subject_detail'),
]
