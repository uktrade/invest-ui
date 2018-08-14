from django.shortcuts import redirect
from django.utils import translation
from django.utils.cache import set_response_etag
from django.http import Http404
from django.conf import settings
from directory_cms_client.client import cms_api_client

from core import helpers


class IncorrectSlug(Exception):
    def __init__(self, canonical_url, *args, **kwargs):
        self.canonical_url = canonical_url
        super().__init__(*args, **kwargs)


class SetEtagMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.method == 'GET':
            response.add_post_render_callback(set_response_etag)
        return response


class ActiveViewNameMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_view_name'] = self.active_view_name
        return context


class GetCMSPageMixin:
    def get_cms_page(self):
        if hasattr(self, 'slug'):
            slug = self.slug
        else:
            slug = self.kwargs['slug']
        response = cms_api_client.lookup_by_slug(
            slug=slug,
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return self.handle_cms_response(response)

    def handle_cms_response(self, response):
        page = helpers.handle_cms_response(response)
        requested_language = translation.get_language()
        if requested_language not in dict(page['meta']['languages']):
            raise Http404('Content not found in requested language.')
        if hasattr(self.kwargs, 'slug') and \
                page['meta']['slug'] != self.kwargs['slug']:
            raise IncorrectSlug(page['meta']['url'])
        return page

    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except IncorrectSlug as exception:
            return redirect(exception.canonical_url)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.get_cms_page(),
            *args,
            **kwargs
        )


class CMSLanguageSwitcherMixin:
    def get_context_data(self, page, *args, **kwargs):
        show_language_switcher = (
            len(page['meta']['languages']) > 1 and
            'en-gb' in page['meta']['languages'][0]
        )
        language_available = translation.get_language() \
            in page['meta']['languages']
        return super().get_context_data(
            language_switcher={
                'show': show_language_switcher,
                'available_languages': page['meta']['languages'],
                'language_available': language_available
            },
            *args,
            **kwargs
        )
