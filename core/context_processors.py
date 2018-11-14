from django.conf import settings
from core.helpers import get_untranslated_url
from directory_components.context_processors import get_url, lazy_build_url


def feature_flags(request):
    return {
        'features': {
        }
    }


def analytics(request):
    return {
        'analytics': {
            'GOOGLE_TAG_MANAGER_ID': settings.GOOGLE_TAG_MANAGER_ID,
            'GOOGLE_TAG_MANAGER_ENV': settings.GOOGLE_TAG_MANAGER_ENV,
            'UTM_COOKIE_DOMAIN': settings.UTM_COOKIE_DOMAIN,
        }
    }


def untranslated_url(request):
    untranslated_url = get_untranslated_url(request.path)
    return {
        'untranslated_url': untranslated_url
    }


international_contact_url = lazy_build_url(
    'HEADER_FOOTER_URLS_GREAT_HOME', 'international/contact/')


def footer_contact_us_link(request):
    feedback_url = get_url('HEADER_FOOTER_URLS_CONTACT_US')

    if settings.FEATURE_FLAGS.get('INTERNATIONAL_CONTACT_LINK_ON'):
        footer_contact_us_link = international_contact_url
    else:
        footer_contact_us_link = feedback_url

    return {
        'footer_contact_us_link': footer_contact_us_link
    }
