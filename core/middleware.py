from django.conf import settings
from django.utils import translation


class PersistLocaleMiddleware:
    def process_response(self, request, response):
        response.set_cookie(
            key=settings.LANGUAGE_COOKIE_NAME,
            value=translation.get_language(),
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN
        )
        return response
