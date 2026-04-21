from django.views.generic import ListView
from .models import Result


class ResultListView(ListView):
    model = Result
    template_name = 'results/result_list.html'
    context_object_name = 'results'
