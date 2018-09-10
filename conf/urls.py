from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url, include
from django.contrib.sitemaps.views import sitemap

import contact.views
import core.views
import conf.sitemaps
import invest.views
from conf.urls_redirect import QuerystringRedirectView

from . import urls_redirect

import directory_components.views

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
        directory_components.views.RobotsView.as_view(),
        name='robots'
    ),
    url(r'', include(urls_redirect)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    url(
        r'^feedback/$',
        QuerystringRedirectView.as_view(
            url='https://contact-us.export.great.gov.uk/directory/FeedbackForm/',  # NOQA
            permanent=True
        )
    ),
    url(
        r'^terms-and-conditions/$',
        QuerystringRedirectView.as_view(
            url='https://www.great.gov.uk/terms-and-conditions/',
            permanent=True
        )
    ),
    url(
        r'^privacy-and-cookies/$',
        QuerystringRedirectView.as_view(
            url='https://www.great.gov.uk/privacy-and-cookies/',
            permanent=True
        )
    ),
    url(
        r"^$",
        core.views.LandingPageCMSView.as_view(),
        name="index"
    ),
    url(
        r"^industries/$",
        core.views.IndustriesLandingPageCMSView.as_view(),
        name="industries"
    ),
    url(
        r"^industries/(?P<parent_slug>[\w-]+)/(?P<slug>[\w-]+)/$",
        core.views.IndustryPageCMSView.as_view(),
        name="industry"
    ),
    url(
        r"^industries/(?P<slug>[\w-]+)/$",
        core.views.IndustryPageCMSView.as_view(),
        name="industry"
    ),
    url(
        r"^uk-setup-guide/$",
        core.views.SetupGuideLandingPageCMSView.as_view(),
        name="setup-guide"
    ),
    url(
        r"^uk-setup-guide/(?P<slug>[\w-]+)/$",
        core.views.SetupGuidePageCMSView.as_view(),
        name="guide-page"
    ),
    url(
        r"^uk-regions/(?P<slug>[\w-]+)/$",
        core.views.UKRegionPageCMSView.as_view(),
        name="uk-region"
    ),
    url(
        r'^high-potential-opportunities/(?P<opportunity_slug>[-\w\d]+)/$',
        invest.views.HighPotentialOpportunityFormView.as_view(),
        name='high-potential-opportunity-details-request-form'
    ),
    url(
        r"^contact/$",
        contact.views.ContactFormView.as_view(),
        name="contact"
    ),
    url(
        r"^contact/success/$",
        contact.views.ContactFormSuccessView.as_view(),
        name="contact-success"
    ),
    prefix_default_language=False,
)
