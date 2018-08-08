import pytest
import requests

from django.shortcuts import Http404

from core import helpers
import core.tests.helpers


@pytest.mark.parametrize('status_code,exception', (
    (400, requests.exceptions.HTTPError),
    (404, Http404),
    (500, requests.exceptions.HTTPError),
))
def test_handle_cms_response_error(status_code, exception):
    response = core.tests.helpers.create_response(status_code=status_code)
    with pytest.raises(exception):
        helpers.handle_cms_response(response)


def test_handle_cms_response_ok():
    response = core.tests.helpers.create_response(
        status_code=200, json_payload={'field': 'value'}
    )

    assert helpers.handle_cms_response(response) == {'field': 'value'}


@pytest.mark.parametrize('path,expected_prefix', (
    ('/', 'en-gb'),
    ('/ar/', 'ar'),
    ('/es/industries/', 'es'),
    ('/zh-cn/industries/', 'zh-cn'),
    ('/de/industries/aerospace/', 'de'),
    ('/fr/industries/automotive/', 'fr'),
))
def test_get_language_from_prefix(client, path, expected_prefix):
    prefix = helpers.get_language_from_prefix(path)
    assert prefix == expected_prefix


@pytest.mark.parametrize('prefixed_url,exp_url', (
    ('/de/', '/'),
    ('/ar/', '/'),
    ('/es/industries/', '/industries/'),
    ('/zh-cn/industries/', '/industries/'),
    ('/de/industries/aerospace/', '/industries/aerospace/'),
    ('/fr/industries/automotive/', '/industries/automotive/'),
))
def test_get_untranslated_url(prefixed_url, exp_url):
    url = helpers.get_untranslated_url(prefixed_url)
    assert url == exp_url
