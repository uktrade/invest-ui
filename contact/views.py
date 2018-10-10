from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _

from contact import forms, mixins


class ContactFormView(mixins.LanguageSwitcherEnabledMixin, FormView):
    success_url = reverse_lazy('contact-success')
    template_name = 'contact/contact.html'
    form_class = forms.ContactForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['utm_data'] = self.request.utm
        kwargs['submission_url'] = self.request.path
        return kwargs

    def form_valid(self, form):
        if settings.FEATURE_FLAGS['FORMS_API_ON']:
            form.save()
        else:
            self.send_user_email(form)
            self.send_agent_email(form)
        return super().form_valid(form)

    @staticmethod
    def send_user_email(form):
        send_mail(
            _('Contact form user email subject'),
            '',
            settings.DEFAULT_FROM_EMAIL,
            [form.cleaned_data['email']],
            fail_silently=False,
            html_message=form.render_email('email/email_user.html'),
        )

    @staticmethod
    def send_agent_email(form):
        send_mail(
            _('Contact form user email subject'),
            '',
            settings.DEFAULT_FROM_EMAIL,
            [settings.IIGB_AGENT_EMAIL],
            fail_silently=False,
            html_message=form.render_email('email/email_agent.html'),
        )


class ContactFormSuccessView(
    mixins.LanguageSwitcherEnabledMixin,
    TemplateView
):
    template_name = 'contact/contact_form_success_page.html'
