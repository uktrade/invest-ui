from django.conf import settings
from django.http import HttpResponse

from core.middleware import PersistLocaleMiddleware


def test_locale_persist_middleware_installed():
    expected = 'core.middleware.PersistLocaleMiddleware'
    assert expected in settings.MIDDLEWARE_CLASSES


def test_locale_persist_middleware_handles_no_explicit_language(client, rf):
    request = rf.get('/')
    response = HttpResponse()
    request.session = client.session
    instance = PersistLocaleMiddleware()

    instance.process_response(request, response)

    cookie = response.cookies[settings.LANGUAGE_COOKIE_NAME]
    assert cookie.value == settings.LANGUAGE_CODE


def test_locale_persist_middleware_persists_explicit_language(client, rf):
    language_code = 'en-gb'
    request = rf.get('/', {'lang': language_code})
    response = HttpResponse()
    request.session = client.session
    instance = PersistLocaleMiddleware()

    instance.process_response(request, response)
    cookie = response.cookies[settings.LANGUAGE_COOKIE_NAME]

    assert cookie.value == language_code
