from unittest.mock import patch, PropertyMock, Mock, call
import pytest

from bs4 import BeautifulSoup

from django.utils import translation
from django.http import Http404
from django.urls import reverse
from django.conf import settings as django_settings

from core.views import CMSPageView, IndustryPageCMSView
from core.mixins import GetSlugFromKwargsMixin
from core import helpers
from directory_constants import urls


test_sectors = [
    {
        'title': 'Aerospace',
        'featured': True,
        'meta': {
            'slug': 'invest-aerospace',
            'languages': [
                ['en-gb', 'English'],
                ['ar', 'العربيّة'],
                ['de', 'Deutsch'],
            ],
        },
    },
    {
        'title': 'Automotive',
        'featured': True,
        'meta': {
            'slug': 'invest-automotive',
            'languages': [
                ['en-gb', 'English'],
                ['fr', 'Français'],
                ['ja', '日本語'],
            ],
        },
    },
]

dummy_page = {
    'title': 'test',
    'children_sectors': [],
    'meta': {
        'languages': [
            ['en-gb', 'English'],
            ['fr', 'Français'],
            ['de', 'Deutsch'],
        ]
    }
}


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_cms_language_switcher_one_language(mock_cms_response, rf):
    class MyView(CMSPageView):

        template_name = 'core/base.html'
        slug = 'test'
        active_view_name = ''

    page = {
        'title': 'test',
        'meta': {
            'languages': [
                ['de', 'Deutsch'],
            ]
        }
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/')
    with translation.override('de'):
        response = MyView.as_view()(request)

    assert response.status_code == 200
    assert response.context_data['language_switcher']['show'] is False


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_cms_language_switcher_active_language_available(
    mock_cms_response, rf
):
    class MyView(CMSPageView):

        template_name = 'core/base.html'
        slug = 'test'
        active_view_name = ''

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=dummy_page
    )

    request = rf.get('/de/')
    with translation.override('de'):
        response = MyView.as_view()(request)

    assert response.status_code == 200
    context = response.context_data['language_switcher']
    assert context['show'] is True


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_active_view_name(mock_cms_response, rf):
    class TestView(CMSPageView):
        active_view_name = 'test'
        template_name = 'core/base.html'
        slug = 'test'

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=dummy_page
    )

    request = rf.get('/')
    response = TestView.as_view()(request)

    assert response.status_code == 200
    assert response.context_data['active_view_name'] == 'test'


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_get_cms_page(mock_cms_response, rf):
    class TestView(CMSPageView):
        template_name = 'core/base.html'
        slug = 'invest-home-page'
        active_view_name = ''

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=dummy_page
    )

    request = rf.get('/')
    response = TestView.as_view()(request)

    assert response.context_data['page'] == dummy_page


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_get_cms_page_kwargs_slug(mock_cms_response, rf):
    class TestView(GetSlugFromKwargsMixin, CMSPageView):
        template_name = 'core/base.html'
        active_view_name = ''

    page = {
        'title': 'the page',
        'meta': {
            'languages': [('en-gb', 'English'), ('de', 'German')],
            'slug': 'aerospace'
        },
    }

    mock_cms_response.return_value = helpers.create_response(
            status_code=200,
            json_payload=page
        )

    translation.activate('en-gb')
    request = rf.get('/')
    view = TestView.as_view()
    response = view(request, slug='aerospace')

    assert response.context_data['page'] == page


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_404_when_cms_language_unavailable(mock_cms_response, rf):
    class TestView(GetSlugFromKwargsMixin, CMSPageView):
        template_name = 'core/base.html'

    page = {
        'title': 'the page',
        'meta': {
            'languages': [('en-gb', 'English'), ('de', 'German')],
            'slug': 'aerospace'
        },
    }

    mock_cms_response.return_value = helpers.create_response(
            status_code=200,
            json_payload=page
        )

    translation.activate('fr')
    request = rf.get('/fr/')
    view = TestView.as_view()

    with pytest.raises(Http404):
        view(request, slug='aerospace')


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@patch('core.views.LandingPageCMSView.page', new_callable=PropertyMock)
def test_landing_page_cms_component(
    mock_get_page, mock_get_component, client, settings
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'EU_EXIT_BANNER_ON': True,
    }
    mock_get_page.return_value = {
        'title': 'the page',
        'sectors': [],
        'guides': [],
        'high_potential_opportunities': [],
        'featured_cards': [],
        'meta': {'languages': [('en-gb', 'English')]},
    }
    mock_get_component.return_value = helpers.create_response(
            status_code=200,
            json_payload={
                'banner_label': 'EU Exit updates',
                'banner_content': '<p>Lorem ipsum.</p>',
                'meta': {'languages': [('en-gb', 'English')]},
            }
    )

    url = reverse('index')
    response = client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    assert soup.select('.banner-container')[0].get('dir') == 'ltr'
    assert response.template_name == ['core/landing_page.html']
    assert 'EU Exit updates' in str(response.content)
    assert '<p class="body-text">Lorem ipsum.</p>' in str(response.content)


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@patch('core.views.LandingPageCMSView.page', new_callable=PropertyMock)
def test_landing_page_cms_component_bidi(
    mock_get_page, mock_get_component, client, settings
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'EU_EXIT_BANNER_ON': True,
    }
    mock_get_page.return_value = {
        'title': 'the page',
        'sectors': [],
        'guides': [],
        'high_potential_opportunities': [],
        'featured_cards': [],
        'meta': {'languages': [('ar', 'العربيّة')]},
    }
    mock_get_component.return_value = helpers.create_response(
            status_code=200,
            json_payload={
                'banner_label': 'EU Exit updates',
                'banner_content': '<p>Lorem ipsum.</p>',
                'meta': {'languages': [('ar', 'العربيّة')]},
            }
    )

    translation.activate('ar')
    url = reverse('index')
    response = client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    assert soup.select('.banner-container')[0].get('dir') == 'rtl'


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@patch('core.views.LandingPageCMSView.page', new_callable=PropertyMock)
def test_localised_urls(mock_get_page, mock_get_component, client):
    mock_get_page.return_value = {
        'title': 'test',
        'sectors': [],
        'guides': [],
        'high_potential_opportunities': [],
        'featured_cards': [],
        'meta': {
            'languages': [
                ('en-gb', 'English'),
                ('fr', 'Français'),
                ('de', 'Deutsch'),
                ['ja', '日本語'],
            ]
        }
    }
    mock_get_component.return_value = helpers.create_response(
            status_code=200,
            json_payload={
                'banner_label': 'EU Exit updates',
                'banner_content': '<p>Lorem ipsum.</p>',
                'meta': {'languages': [('en-gb', 'English')]}
            }
    )

    translation.activate('de')
    url = reverse('index')
    response = client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    assert not soup.select('link[hreflang="de"]')
    assert soup.select('link[hreflang="fr"]')
    assert soup.select('link[hreflang="ja"]')
    assert soup.select('link[hreflang="en-gb"]')


@pytest.mark.parametrize('url', (
    'contact',
    'contact-success'
))
def test_contact_pages_localised_urls(url, client):
    translation.activate('de')
    url = reverse(url)
    response = client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    other_languages = [
        code for code, _ in django_settings.LANGUAGES if code != 'de']

    for code in other_languages:
        link_tag = soup.select(f'link[hreflang="{code}"]')[0]
        assert link_tag
        assert 'http://testserver' in link_tag.attrs['href']
        if code != 'en-gb':
            assert code in link_tag.attrs['href']


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_industry_page_exists_in_international(mock_get_page, client):
    mocked_response = Mock(status_code=200)
    mocked_response.json.return_value = {'full_url': 'http://test.com'}
    mock_get_page.return_value = mocked_response
    url = reverse('industry', kwargs={'slug': 'foo'})
    response = client.get(url)
    assert mock_get_page.call_args == call(draft_token=None,
                                           language_code='en-gb',
                                           service_name='GREAT_INTERNATIONAL',
                                           slug='foo')
    assert response.status_code == 302
    assert response.url == 'http://test.com'


@patch.object(IndustryPageCMSView, 'international_industry_page_exists',
              new_callable=PropertyMock)
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_industry_page_does_not_exist_in_international(mock_get_page,
                                                       mock_page_exists,
                                                       client):
    mock_page_exists.return_value = None
    mock_get_page.return_value = helpers.create_response(
        status_code=200,
        json_payload=dummy_page
    )
    url = reverse('industry', kwargs={'slug': 'foo'})
    response = client.get(url)
    assert mock_get_page.call_args == call(draft_token=None,
                                           language_code='en-gb',
                                           slug='foo')
    assert response.status_code == 200


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@patch('core.views.LandingPageCMSView.page', new_callable=PropertyMock)
def test_get_int_link_on_invest_home_page(
        mock_get_page, mock_get_component, client):

    mock_get_page.return_value = {
        'title': 'the page',
        'high_potential_opportunities': [],
        'featured_cards': [],
        'meta': {'languages': [('en-gb', 'English')]},
    }
    mock_get_component.return_value = helpers.create_response(
        status_code=200,
        json_payload=dummy_page
    )

    url = reverse('index')
    response = client.get(url)

    assert response.context_data[
               'international_home_page_link'] == urls.GREAT_INTERNATIONAL


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@patch('core.views.LandingPageCMSView.page', new_callable=PropertyMock)
def test_show_hpo_section(mock_get_page, mock_get_component, client):
    mock_get_page.return_value = {
        'title': 'the page',
        'high_potential_opportunities': [
            {
                'title': 'Rail Infrastructure',
                'meta': {
                    'slug': 'invest-aerospace',
                    'languages': [
                        ['fr', 'Français'],
                    ],
                },
            },
        ],
        'featured_cards': [],
        'meta': {'languages': [('en-gb', 'English')]},
    }
    mock_get_component.return_value = helpers.create_response(
        status_code=200,
        json_payload=dummy_page
    )

    url = reverse('index')
    response = client.get(url)

    assert response.context_data['show_hpo_section'] is False


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@patch('core.views.LandingPageCMSView.page', new_callable=PropertyMock)
def test_show_featured_cards_section(
        mock_get_page,
        mock_get_component,
        client
):
    mock_get_page.return_value = {
        'title': 'the page',
        'featured_cards': [
            {
                'title': 'Get started in the UK',
                'image': {
                    'url': 'https://directory-cms-public.s3.amazonaws.com'
                           '/images/Get_started_in_the_UK.2e16d0ba.'
                           'fill-640x360_i3FI8OQ.jpg',
                    'width': 640,
                    'height': 360
                },
                'summary': 'A summary',
            },
            {
                'title': 'Get started in the UK',
                'image': {
                    'url': 'https://directory-cms-public.s3.amazonaws.com'
                           '/images/Get_started_in_the_UK.2e16d0ba.'
                           'fill-640x360_i3FI8OQ.jpg',
                    'width': 640,
                    'height': 360
                },
                'summary': 'A summary',
                'cta_link': 'www.google.com'
            },
            {
                'title': 'Get started in the UK',
                'image': {
                    'url': 'https://directory-cms-public.s3.amazonaws.com'
                           '/images/Get_started_in_the_UK.2e16d0ba.'
                           'fill-640x360_i3FI8OQ.jpg',
                    'width': 640,
                    'height': 360
                },
                'summary': 'A summary',
            },
        ],
        'high_potential_opportunities': [],
        'meta': {'languages': [('en-gb', 'English')]},
    }
    mock_get_component.return_value = helpers.create_response(
        status_code=200,
        json_payload=dummy_page
    )

    url = reverse('index')
    response = client.get(url)

    assert response.context_data['show_featured_cards'] is True


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@patch('core.views.LandingPageCMSView.page', new_callable=PropertyMock)
def test_show_featured_cards_section_doesnt_show_when_not_all_there(
        mock_get_page,
        mock_get_component,
        client
):
    mock_get_page.return_value = {
        'title': 'the page',
        'featured_cards': [
            {
                'title': '',
                'image': {},
                'summary': 'A summary',
            },
            {
                'title': 'Get started in the UK',
                'image': {},
                'summary': 'A summary',
                'cta_link': 'www.google.com'
            },
            {
                'title': 'Get started in the UK',
                'image': {},
                'summary': '',
            },
        ],
        'high_potential_opportunities': [],
        'meta': {'languages': [('en-gb', 'English')]},
    }
    mock_get_component.return_value = helpers.create_response(
        status_code=200,
        json_payload=dummy_page
    )

    url = reverse('index')
    response = client.get(url)

    assert response.context_data['show_featured_cards'] is False
