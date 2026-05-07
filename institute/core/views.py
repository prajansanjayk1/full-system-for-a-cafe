from django.views.generic import TemplateView
from courses.models import Course
from results.models import Result
from testimonials.models import Testimonial
from blog.models import BlogPost
from core.models import SiteSettings


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()[:3]
        context['results'] = Result.objects.all()[:6]
        context['testimonials'] = Testimonial.objects.all()[:3]
        context['blogs'] = BlogPost.objects.all()[:3]
        context['meta_title'] = 'Tuition Centre in Tambaram | SD Institute'
        context['meta_description'] = 'Premium coaching for Class 9–12 students with concept-first learning and measurable academic improvement.'
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings = SiteSettings.objects.first()
        context['meta_title'] = f'About {settings.institute_name if settings else "Institute"}'
        context['meta_description'] = 'Learn about our teaching methodology, mentors, and student-focused approach in Tambaram, Chennai.'
        return context
