from django.conf import settings
from core.helpers import get_untranslated_url


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
    untranslated_url = get_untranslated_url(request)
    return {
        'untranslated_url': untranslated_url
    }
