from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import ContactForm


class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:contact_page')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Thanks for contacting us. We will reach out shortly.')
        return super().form_valid(form)
