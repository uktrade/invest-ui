from django.shortcuts import redirect
from django.utils import translation
from django.utils.cache import set_response_etag
from django.http import Http404

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


class ChildPageLocalSlugs:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for page_group_name in self.subpage_groups:
            pages = context['page'][page_group_name]
            for page in pages:
                page['meta']['slug'] = page['meta']['slug'][7:]
            localised_subpages = 'localised_{}'.format(page_group_name)
            context[localised_subpages] = pages
         return context


class GetCMSPageMixin:
    def get_cms_page(self):
        response = helpers.cms_client.lookup_by_slug(
            slug=self.kwargs['slug'],
            draft_token=self.request.GET.get('draft_token'),
            language_code=translation.get_language(),
        )
        return self.handle_cms_response(response)

    def handle_cms_response(self, response):
        page = helpers.handle_cms_response(response)
        requested_language = translation.get_language()
        if requested_language not in dict(page['meta']['languages']):
            raise Http404
        if page['meta']['slug'] != self.kwargs['slug']:
            raise IncorrectSlug(page['meta']['url'])
        return page

    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except IncorrectSlug as exception:
            return redirect(exception.canonical_url)


class CMSLanguageSwitcherMixin:
    def get_context_data(self, page, *args, **kwargs):
        show_language_switcher = (
            len(page['meta']['languages']) > 1 and
            'en-gb' in page['meta']['languages'][0]
        )
        language_available = translation.get_language() \
            in page['meta']['languages']
        return super().get_context_data(
            page=page,
            language_switcher={
                'show': show_language_switcher,
                'available_languages': page['meta']['languages'],
                'language_available': language_available
            },
            *args,
            **kwargs
        )
