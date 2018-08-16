from django.views.generic import TemplateView

from core import mixins


class CMSPageView(
    mixins.CMSLanguageSwitcherMixin,
    mixins.GetCMSPageMixin,
    mixins.ActiveViewNameMixin,
    TemplateView
):
    pass


class LandingPageCMSView(CMSPageView):
    active_view_name = 'index'
    template_name = 'core/landing_page.html'
    slug = 'invest-home-page'
    app = 'invest'
    subpage_groups = ['sectors', 'guides']


class IndustriesLandingPageCMSView(CMSPageView):
    active_view_name = 'industries'
    template_name = 'core/industries_landing_page.html'
    slug = 'invest-sector-landing-page'
    service = 'invest'
    subpage_groups = ['children_sectors']


class IndustryPageCMSView(CMSPageView):
    active_view_name = 'industries'
    template_name = 'core/industry_page.html'
    subpage_groups = ['children_sectors']


class SetupGuideLandingPageCMSView(CMSPageView):
    active_view_name = 'setup-guide'
    template_name = 'core/setup_guide_landing_page.html'
    slug = 'invest-setup-guide-landing-page'
    subpage_groups = ['children_setup_guides']


class SetupGuidePageCMSView(CMSPageView):
    active_view_name = 'setup-guide'
    template_name = 'core/accordion_content_page.html'


class UKRegionPageCMSView(SetupGuidePageCMSView):
    active_view_name = ''
