from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import RegistrationForm


class RegistrationCreateView(FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('registration:register')

    def form_valid(self, form):
        registration = form.save()
        email_body = (
            f"New Demo Class Registration\n\n"
            f"Student Name: {registration.student_name}\n"
            f"Class: {registration.get_class_level_display()}\n"
            f"Subject Interest: {registration.subject_interest}\n"
            f"Parent Name: {registration.parent_name}\n"
            f"Phone Number: {registration.phone_number}\n"
            f"Email: {registration.email}\n"
            f"Message: {registration.message or 'N/A'}\n"
        )
        send_mail(
            subject='New Registration - Tuition Demo Request',
            message=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_NOTIFICATION_EMAIL],
            fail_silently=False,
        )
        messages.success(self.request, 'Registration successful! Our team will contact you soon.')
        return super().form_valid(form)
