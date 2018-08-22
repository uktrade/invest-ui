from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from contact import forms, mixins


class ContactFormView(mixins.LanguageSwitcherEnabledMixin, FormView):
    success_url = reverse_lazy('contact-success')
    template_name = 'contact/contact.html'
    form_class = forms.ContactForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['utm_data'] = self.request.utm
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ContactFormSuccessView(
    mixins.LanguageSwitcherEnabledMixin,
    TemplateView
):
    template_name = 'contact/contact_form_success_page.html'
