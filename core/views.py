from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils.functional import cached_property
from django.utils import translation
from django.http import Http404
from directory_cms_client.client import cms_api_client
from directory_components.mixins import (
    CountryDisplayMixin, LanguageSwitcherMixin
)

from core.mixins import (
    GetCMSComponentMixin, GetSlugFromKwargsMixin, LocalisedURLsMixin)
from directory_cms_client.helpers import handle_cms_response
from directory_constants.constants import cms, urls


class IncorrectSlug(Exception):
    def __init__(self, canonical_url, *args, **kwargs):
        self.canonical_url = canonical_url
        super().__init__(*args, **kwargs)


class CMSPageView(
    LocalisedURLsMixin,
    CountryDisplayMixin,
    LanguageSwitcherMixin,
    TemplateView
):
    @property
    def available_languages(self):
        return self.page['meta']['languages']

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_slug(
            slug=self.slug,
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return self.handle_cms_response(response)

    def handle_cms_response(self, response):
        page = handle_cms_response(response)
        requested_language = translation.get_language()
        if requested_language not in dict(page['meta']['languages']):
            raise Http404('Content not found in requested language.')
        return page

    def get_context_data(self, *args, **kwargs):
        page = self.page
        show_language_switcher = (
            len(page['meta']['languages']) > 1 and
            'en-gb' in page['meta']['languages'][0]
        )
        language_available = translation.get_language() \
            in page['meta']['languages']

        return super().get_context_data(
            language_switcher={
                'show': show_language_switcher,
                'available_languages': self.available_languages,
                'language_available': language_available
            },
            page=page,
            active_view_name=self.active_view_name,
            *args,
            **kwargs
        )


class LandingPageCMSView(GetCMSComponentMixin, CMSPageView):
    active_view_name = 'index'
    template_name = 'core/landing_page.html'
    component_slug = cms.COMPONENTS_BANNER_INTERNATIONAL_SLUG
    slug = 'home-page'
    subpage_groups = ['sectors', 'guides']

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            set_up_in_uk_international_link=(
                urls.GREAT_INTERNATIONAL_HOW_TO_SETUP_IN_THE_UK
            ),
            capital_invest_landing_page_link=(
                urls.GREAT_INTERNATIONAL_CAPITAL_INVEST_LANDING_PAGE
            ),
            how_to_do_business_link=(
                urls.GREAT_INTERNATIONAL_HOW_TO_DO_BUSINESS_WITH_THE_UK
            ),
            **kwargs
        )


class IndustriesLandingPageCMSView(CMSPageView):
    active_view_name = 'industries'
    template_name = 'core/industries_landing_page.html'
    slug = 'sector-landing-page'
    subpage_groups = ['children_sectors']


class IndustryPageCMSView(GetSlugFromKwargsMixin, CMSPageView):
    active_view_name = 'industries'
    template_name = 'core/industry_page.html'
    subpage_groups = ['children_sectors']

    @cached_property
    def international_industry_page_exists(self):
        response = cms_api_client.lookup_by_slug(
            slug=self.slug,
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
            service_name=cms.GREAT_INTERNATIONAL
        )
        if response.status_code == 200:
            return response.json()
        return None

    def dispatch(self, request, *args, **kwargs):
        page = self.international_industry_page_exists
        if page:
            return redirect(page['full_url'])
        return super().dispatch(request, *args, **kwargs)


class SetupGuideLandingPageCMSView(CMSPageView):
    active_view_name = 'setup-guide'
    template_name = 'core/setup_guide_landing_page.html'
    slug = 'setup-guide-landing-page'
    subpage_groups = ['children_setup_guides']


class SetupGuidePageCMSView(GetSlugFromKwargsMixin, CMSPageView):
    active_view_name = 'setup-guide'
    template_name = 'core/accordion_content_page.html'


class UKRegionPageCMSView(GetSlugFromKwargsMixin, CMSPageView):
    active_view_name = ''
    template_name = 'core/accordion_content_page_with_hero_image.html'
