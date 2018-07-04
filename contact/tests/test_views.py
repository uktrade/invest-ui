import pytest
from django.urls import reverse, reverse_lazy
from unittest.mock import patch
from django.core import mail

from contact import forms
from contact.views import ContactFormView


@pytest.fixture
def contact_form_data():
    return {
        'name': 'Scrooge McDuck',
        'email': 'sm@example.com',
        'job_title': 'President',
        'phone_number': '0000000000',
        'company_name': 'Acme',
        'country': 'United States',
        'staff_number': forms.STAFF_CHOICES[0][0],
        'description': 'foobar',
    }


@pytest.mark.django_db
@patch('captcha.fields.ReCaptchaField.clean')
def test_contact_form(
    mock_clean_captcha,
    contact_form_data,
    settings,
    client
):
    mail.outbox = []

    settings.IIGB_AGENT_EMAIL = "agent@email.com"

    url = reverse('contact')
    response = client.post(url, data=contact_form_data)

    assert response.status_code == 302
    assert response.url == reverse_lazy('contact-success')
    assert len(mail.outbox) == 2

    agent_email, user_email = mail.outbox

    if agent_email.to != [settings.IIGB_AGENT_EMAIL]:
        agent_email, user_email = user_email, agent_email

    assert agent_email.to == [settings.IIGB_AGENT_EMAIL]
    assert user_email.to == [contact_form_data["email"]]

    form_data = ContactFormView.extract_data(contact_form_data)

    for email in [agent_email, user_email]:
        body = email.alternatives[0][0]
        for field, value in form_data:
            assert '<td>{field}</td>'.format(field=field) in body, field
            assert '<td>{value}</td>'.format(value=value) in body, value

    assert mock_clean_captcha.call_count == 1


@pytest.mark.django_db
@patch('captcha.fields.ReCaptchaField.clean')
def test_contact_page_agent_email_utm_codes(
    mock_clean_captcha,
    contact_form_data,
    settings,
    rf
):
    mail.outbox = []

    settings.IIGB_AGENT_EMAIL = "agent@email.com"

    utm_codes = {
        'utm_source': 'test_source',
        'utm_medium': 'test_medium',
        'utm_campaign': 'test_campaign',
        'utm_term': 'test_term',
        'utm_content': 'test_content'
    }

    url = reverse('contact')

    request = rf.post(url, contact_form_data)
    request.utm = utm_codes
    ContactFormView.as_view()(request)

    assert len(mail.outbox) == 2

    if mail.outbox[0].to == [settings.IIGB_AGENT_EMAIL]:
        agent_email = mail.outbox[0]
    else:
        agent_email = mail.outbox[1]

    body = agent_email.alternatives[0][0]
    for code, value in utm_codes.items():
        assert '{code}: {value}'.format(code=code, value=value) in body, code
