from contact import forms


def test_contact_form_required():
    form = forms.ContactForm()

    assert form.is_valid() is False
    assert form.fields['name'].required is True
    assert form.fields['email'].required is True
    assert form.fields['job_title'].required is True
    assert form.fields['phone_number'].required is True
    assert form.fields['company_name'].required is True
    assert form.fields['company_website'].required is False
    assert form.fields['country'].required is True
    assert form.fields['staff_number'].required is True
    assert form.fields['description'].required is True
    assert form.fields['captcha'].required is True


def test_contact_form_accept_valid_data(captcha_stub):
    form = forms.ContactForm(
        data={
            'name': 'Scrooge McDuck',
            'email': 'sm@example.com',
            'phone_number': '0000000000',
            'job_title': 'President',
            'company_name': 'Acme',
            'country': 'United States',
            'staff_number': forms.STAFF_CHOICES[0][0],
            'description': 'foobar',
            'recaptcha_response_field': captcha_stub
        }
    )
    assert form.is_valid()
