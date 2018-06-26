from django.utils import translation
from django.views.generic import TemplateView

from core import mixins


class LandingPageCMSView(
    mixins.CMSLanguageSwitcherMixin, mixins.ActiveViewNameMixin,
    mixins.ChildPageLocalSlugs, mixins.GetCMSPageMixin, TemplateView
):
    active_view_name = 'index'
    template_name = 'core/landing_page.html'
    slug = 'invest-home-page'
    app = 'invest'
    subpage_groups = ['sectors', 'guides']

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.get_cms_page(),
            *args,
            **kwargs
        )


class IndustriesLandingPageCMSView(
    mixins.CMSLanguageSwitcherMixin, mixins.ActiveViewNameMixin,
    mixins.ChildPageLocalSlugs, mixins.GetCMSPageMixin, TemplateView
):
    active_view_name = 'industries'
    template_name = 'core/industries_landing_page.html'
    slug = 'invest-sector-landing-page'
    service = 'invest'
    subpage_groups = ['children_sectors']

    def get_context_data(self, *args, **kwargs):
        page = self.get_cms_page()
        current_language_child_sectors = []
        current_language = translation.get_language()
        for sector in page['children_sectors']:
            if current_language in dict(sector['meta']['languages']):
                current_language_child_sectors.append(sector)
        return super().get_context_data(
            page=page,
            current_language_child_sectors=current_language_child_sectors,
            *args,
            **kwargs
        )


class IndustryPageCMSView(
    mixins.CMSLanguageSwitcherMixin, mixins.GetCMSPageMixin,
    mixins.ChildPageLocalSlugs, mixins.ActiveViewNameMixin, TemplateView
):
    active_view_name = 'industries'
    template_name = 'core/industry_page.html'
    subpage_groups = ['children_sectors']

    def get_context_data(self, *args, **kwargs):
        page = self.get_cms_page()
        has_child_pages = len(page['children_sectors']) > 0
        return super().get_context_data(
            page=page,
            has_child_pages=has_child_pages,
            *args,
            **kwargs
        )


class SetupGuideLandingPageCMSView(
    mixins.CMSLanguageSwitcherMixin, mixins.GetCMSPageMixin,
    mixins.ChildPageLocalSlugs, mixins.ActiveViewNameMixin, TemplateView
):
    active_view_name = 'setup-guide'
    template_name = 'core/setup_guide_landing_page.html'
    slug = 'invest-setup-guide-landing-page'
    subpage_groups = ['children_setup_guides']

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.get_cms_page(),
            *args,
            **kwargs
        )


class SetupGuidePageCMSView(
    mixins.CMSLanguageSwitcherMixin, mixins.GetCMSPageMixin,
    mixins.ActiveViewNameMixin, TemplateView
):
    active_view_name = 'setup-guide'
    template_name = 'core/setup_guide_page.html'

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.get_cms_page(),
            *args,
            **kwargs
        )


class PlainCMSPageView(
    mixins.GetCMSPageMixin, TemplateView
):
    template_name = 'core/plain_cms_page.html'
