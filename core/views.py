from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils.functional import cached_property
from django.utils import translation
from django.http import Http404
from directory_cms_client.client import cms_api_client
from directory_components.mixins import (
    CountryDisplayMixin,
    GA360Mixin)

from core.mixins import (
    GetCMSComponentMixin, GetSlugFromKwargsMixin, LocalisedURLsMixin,
    InvestLanguageSwitcherMixin, InternationalHeaderMixin)
from directory_cms_client.helpers import handle_cms_response
from directory_constants import cms, urls, slugs
from core.templatetags.cms_tags import filter_by_active_language
from core.helpers import count_data_with_field


class IncorrectSlug(Exception):
    def __init__(self, canonical_url, *args, **kwargs):
        self.canonical_url = canonical_url
        super().__init__(*args, **kwargs)


class CMSPageView(
    InternationalHeaderMixin,
    LocalisedURLsMixin,
    CountryDisplayMixin,
    GA360Mixin,
    InvestLanguageSwitcherMixin,
    TemplateView,
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

        return super().get_context_data(
            page=page,
            active_view_name=self.active_view_name,
            *args,
            **kwargs
        )


class LandingPageCMSView(GetCMSComponentMixin, CMSPageView):
    active_view_name = 'index'
    template_name = 'core/landing_page.html'
    component_slug = slugs.COMPONENTS_BANNER_INTERNATIONAL
    slug = 'home-page'
    subpage_groups = ['sectors', 'guides']

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='InvestLandingPage',
            business_unit='Invest',
            site_section='LandingPage',
        )

    def get_context_data(self, **kwargs):
        pages = self.page['high_potential_opportunities'],
        number_of_featured_cards = 0
        return super().get_context_data(
            international_home_page_link=(
                urls.GREAT_INTERNATIONAL
            ),
            investment_support_directory_link=(
                urls.FAS_INVESTMENT_SUPPORT_DIRECTORY
            ),
            how_to_set_up_visas_and_migration_link=(
                urls.GREAT_INTERNATIONAL_HOW_TO_SET_UP_VISAS_AND_MIGRATION
            ),
            how_to_set_up_tax_and_incentives_link=(
                urls.GREAT_INTERNATIONAL_HOW_TO_SET_UP_TAX_AND_INCENTIVES
            ),
            show_hpo_section=bool(
                pages and filter_by_active_language(pages[0])
            ),
            show_featured_cards=(
                number_of_featured_cards == 3
            ),
            **kwargs
        )


class IndustriesLandingPageCMSView(CMSPageView):
    active_view_name = 'industries'
    template_name = 'core/industries_landing_page.html'
    slug = 'sector-landing-page'
    subpage_groups = ['children_sectors']

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='InvestIndustriesLandingPage',
            business_unit='Invest',
            site_section='Industries',
            site_subsection='ListingPage'
        )


class IndustryPageCMSView(GetSlugFromKwargsMixin, CMSPageView):
    active_view_name = 'industries'
    template_name = 'core/industry_page.html'
    subpage_groups = ['children_sectors']

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='InvestIndustryPage',
            business_unit='Invest',
            site_section='Industries',
            site_subsection='DetailPage'
        )

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


class UKRegionPageCMSView(GetSlugFromKwargsMixin, CMSPageView):
    active_view_name = ''
    template_name = 'core/accordion_content_page.html'

    @property
    def international_header_area(self):
        return "about_uk"

    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='InvestUkRegionPage',
            business_unit='Invest',
            site_section='Regions',
            site_subsection='DetailPage'
        )
