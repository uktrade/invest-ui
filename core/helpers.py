from directory_cms_client import DirectoryCMSClient

from django.conf import settings
from django.shortcuts import Http404
from django.utils import translation


cms_client = DirectoryCMSClient(
    base_url=settings.CMS_URL,
    api_key=settings.CMS_SIGNATURE_SECRET,
)


def handle_cms_response(response):
    if response.status_code == 404:
        raise Http404()
    response.raise_for_status()
    return response.json()


def get_language_from_prefix(request):
    language_codes = translation.trans_real.get_languages()
    prefix = slash_split(request.path)
    if prefix in language_codes:
        return prefix
    else:
        return 'en-gb'


def slash_split(string):
    if string.count("/") == 1:
        return string.split("/")[0]
    else:
        return "".join(string.split("/", 2)[:2])


def get_untranslated_url(request):
    current_language = get_language_from_prefix(request)
    if current_language == 'en-gb':
        untranslated_url = request.path
    else:
        untranslated_url = request.path.replace('/' + current_language, '')
    return untranslated_url


def is_language_available(language_code, available_languages):
    language_choices = available_languages
    language_codes = [code for code, lang in language_choices]
    return language_code in language_codes
