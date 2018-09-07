from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.utils import translation
from django.http import Http404
from directory_cms_client.client import cms_api_client

from core import helpers


class IncorrectSlug(Exception):
    def __init__(self, canonical_url, *args, **kwargs):
        self.canonical_url = canonical_url
        super().__init__(*args, **kwargs)


class CMSPageView(TemplateView):
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
        page = self.get_cms_page()

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
            page=page,
            active_view_name=self.active_view_name,
            *args,
            **kwargs
        )


class LandingPageCMSView(CMSPageView):
    active_view_name = 'index'
    template_name = 'core/landing_page.html'
    slug = 'home-page'
    app = 'invest'
    subpage_groups = ['sectors', 'guides']


class IndustriesLandingPageCMSView(CMSPageView):
    active_view_name = 'industries'
    template_name = 'core/industries_landing_page.html'
    slug = 'sector-landing-page'
    service = 'invest'
    subpage_groups = ['children_sectors']


class IndustryPageCMSView(CMSPageView):
    active_view_name = 'industries'
    template_name = 'core/industry_page.html'
    subpage_groups = ['children_sectors']


class SetupGuideLandingPageCMSView(CMSPageView):
    active_view_name = 'setup-guide'
    template_name = 'core/setup_guide_landing_page.html'
    slug = 'setup-guide-landing-page'
    subpage_groups = ['children_setup_guides']


class SetupGuidePageCMSView(CMSPageView):
    active_view_name = 'setup-guide'
    template_name = 'core/accordion_content_page.html'


class UKRegionPageCMSView(CMSPageView):
    active_view_name = ''
    template_name = 'core/accordion_content_page_with_hero_image.html'
