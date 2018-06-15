from django.forms.fields import Field

from core import forms


REQUIRED_MESSAGE = Field.default_error_messages['required']


def test_contact_form_required():
    form = forms.ContactForm()

    assert form.is_valid() is False
    assert form.fields['name'].required is True
    assert form.fields['job_title'].required is True
    assert form.fields['email'].required is True
    assert form.fields['phone_number'].required is True
    assert form.fields['company_name'].required is True
    assert form.fields['country'].required is True
    assert form.fields['staff_number'].required is True
    assert form.fields['description'].required is True


def test_contact_form_accepts_valid_data(captcha_stub):
    form = forms.ContactForm(data={
        'name': 'Jim Example',
        'job_title': 'Director of Things',
        'email': 'jim@example.com',
        'phone_number': '07123456789',
        'company_name': 'Deutsche Bank',
        'country': 'Germany',
        'staff_number': '10 to 50',
        'description': (
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do '
            'eiusmod tempor incididunt ut labore et dolore magna aliqua.'),
        'recaptcha_response_field': captcha_stub
    })
    assert form.is_valid()
