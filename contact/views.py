from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.core.mail import send_mail

from contact import forms


class ContactFormView(FormView):
    success_url = 'success/'
    template_name = 'contact/contact.html'
    form_class = forms.ContactForm

    def send_user_email(self, user_email, form_data):
        html_body = render_to_string('email/email_user.html',
                                     {'form_data': form_data},
                                     self.request)

        send_mail(_('Contact form user email subject'),
                  '',
                  settings.DEFAULT_FROM_EMAIL,
                  [user_email],
                  fail_silently=False, html_message=html_body)

    def send_agent_email(self, form_data):
        html_body = render_to_string('email/email_agent.html',
                                     {'form_data': form_data},
                                     self.request)

        send_mail(_('Contact form user email subject'),
                  '',
                  settings.DEFAULT_FROM_EMAIL,
                  [settings.IIGB_AGENT_EMAIL],
                  fail_silently=False, html_message=html_body)

    @staticmethod
    def extract_data(data):
        """Return a list of field names and values"""
        # handle not required fields
        if 'phone_number' not in data:
            data['phone_number'] = ''
        if 'company_website' not in data:
            data['company_website'] = ''

        return (
            (_('Name'), data['name']),
            (_('Email'), data['email']),
            (_('Job title'), data['job_title']),
            (_('Phone number'), data['phone_number']),
            (_('Company name'), data['company_name']),
            (_('Company website'), data['company_website']),
            (_('Country'), data['country']),
            (_('Staff number'), data['staff_number']),
            (_('Investment description'), data['description'])
        )

    def create_description(self, raw_data):

        data = ["{}: {}".format(*row) for row in self.extract_data(raw_data)]

        return "\n".join(data)

    def form_valid(self, form):
        form_data = self.extract_data(form.cleaned_data)

        self.send_agent_email(form_data)
        self.send_user_email(form.cleaned_data['email'], form_data)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            language_switcher={
                'show': True,
                'available_languages': settings.LANGUAGES,
                'language_available': True
            },
            **kwargs)
        context['success_message'] = _('Your feedback has been submitted')
        return context


class ContactFormSuccessView(TemplateView):
    template_name = 'contact/contact_form_success_page.html'
