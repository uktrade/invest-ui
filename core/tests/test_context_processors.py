from core import context_processors
from urllib.parse import urljoin

from directory_components import urls


def test_feature_flags_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'core.context_processors.feature_flags' in processors


def test_feature_returns_expected_features(rf, settings):

    actual = context_processors.feature_flags(None)

    assert actual == {
        'features': {},
    }


def test_analytics(rf, settings):
    settings.GOOGLE_TAG_MANAGER_ID = '123'
    settings.GOOGLE_TAG_MANAGER_ENV = '&thing=1'
    settings.UTM_COOKIE_DOMAIN = '.thing.com'

    actual = context_processors.analytics(None)

    assert actual == {
        'analytics': {
            'GOOGLE_TAG_MANAGER_ID': '123',
            'GOOGLE_TAG_MANAGER_ENV': '&thing=1',
            'UTM_COOKIE_DOMAIN': '.thing.com',
        }
    }


def test_analytics_installed(settings):
    processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']

    assert 'directory_components.context_processors.analytics' in processors


def test_footer_contact_link_processor_flag_on_settings(settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'INTERNATIONAL_CONTACT_LINK_ON': True,
    }
    settings.HEADER_FOOTER_URLS_CONTACT_US = 'contact.com/'
    settings.HEADER_FOOTER_URLS_GREAT_HOME = 'great.com/'

    actual = context_processors.footer_contact_us_link(None)

    assert actual['footer_contact_us_link'] == (
        'great.com/international/contact/')


def test_footer_contact_link_processor_flag_on_defaults(settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'INTERNATIONAL_CONTACT_LINK_ON': True,
    }
    settings.HEADER_FOOTER_URLS_GREAT_HOME = None

    actual = context_processors.footer_contact_us_link(None)
    expected = urljoin(
        urls.HEADER_FOOTER_URLS_GREAT_HOME, 'international/contact/')

    assert actual['footer_contact_us_link'] == expected


def test_footer_contact_link_processor_flag_off_defaults(settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'INTERNATIONAL_CONTACT_LINK_ON': False,
    }
    settings.HEADER_FOOTER_URLS_CONTACT_US = None

    actual = context_processors.footer_contact_us_link(None)

    assert actual['footer_contact_us_link'] == (
        urls.HEADER_FOOTER_URLS_CONTACT_US)
