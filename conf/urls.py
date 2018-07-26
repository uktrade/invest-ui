from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from contact.views import ContactFormView, ContactFormSuccessView
from core import views

import conf.sitemaps
from . import urls_redirect

sitemaps = {
    'static': conf.sitemaps.StaticViewSitemap,
}

urlpatterns = [
    url(
        r"^sitemap\.xml$", sitemap, {'sitemaps': sitemaps},
        name='sitemap'
    ),
    url(
        r"^robots\.txt$",
        TemplateView.as_view(
            template_name='robots.txt', content_type='text/plain'
        ),
        name='robots'
    ),
    url(r'', include(urls_redirect)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    url(
        r"^$",
        views.LandingPageCMSView.as_view(),
        name="index"
    ),
    url(
        r"^industries/$",
        views.IndustriesLandingPageCMSView.as_view(),
        name="industries"
    ),
    url(
        r"^industries/(?P<parent_slug>[\w-]+)/(?P<slug>[\w-]+)/$",
        views.IndustryPageCMSView.as_view(),
        name="industry"
    ),
    url(
        r"^industries/(?P<slug>[\w-]+)/$",
        views.IndustryPageCMSView.as_view(),
        name="industry"
    ),
    url(
        r"^uk-setup-guide/$",
        views.SetupGuideLandingPageCMSView.as_view(),
        name="setup-guide"
    ),
    url(
        r"^uk-setup-guide/(?P<slug>[\w-]+)/$",
        views.SetupGuidePageCMSView.as_view(),
        name="guide-page"
    ),
    url(
        r"^contact/$",
        ContactFormView.as_view(),
        name="contact"
    ),
    url(
        r"^contact/success/$",
        ContactFormSuccessView.as_view(),
        name="contact-success"
    ),
    url(
        r"^(?P<slug>[\w-]+)/$",
        views.PlainCMSPageView.as_view(),
        name="cms-page"
    ),
    prefix_default_language=False,
)
