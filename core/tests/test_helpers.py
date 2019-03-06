import pytest

from core import helpers


@pytest.mark.parametrize('path,expected_prefix', (
    ('/', 'en-gb'),
    ('/ar/', 'ar'),
    ('/es/industries/', 'es'),
    ('/zh-hans/industries/', 'zh-hans'),
    ('/de/industries/aerospace/', 'de'),
    ('/fr/industries/free-foods/', 'fr'),
))
def test_get_language_from_prefix(client, path, expected_prefix):
    prefix = helpers.get_language_from_prefix(path)
    assert prefix == expected_prefix


@pytest.mark.parametrize('prefixed_url,exp_url', (
    ('/de/', '/'),
    ('/ar/', '/'),
    ('/es/industries/', '/industries/'),
    ('/zh-hans/industries/', '/industries/'),
    ('/de/industries/aerospace/', '/industries/aerospace/'),
    ('/fr/industries/free-foods/', '/industries/free-foods/'),
    (
        '/es/uk-setup-guide/establish-base-business-uk/',
        '/uk-setup-guide/establish-base-business-uk/'
    ),
))
def test_get_untranslated_url(prefixed_url, exp_url):
    url = helpers.get_untranslated_url(prefixed_url)
    assert url == exp_url
