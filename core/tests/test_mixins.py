import pytest
import requests_mock
from unittest.mock import patch

from django.views.generic import TemplateView
from django.utils import translation
from django.http import Http404

from core import mixins, helpers

test_sectors = [
    {
        'title': 'Aerospace',
        'featured': True,
        'meta': {
            'slug': 'invest-aerospace'
        },
    },
    {
        'title': 'Automotive',
        'featured': True,
        'meta': {
            'slug': 'invest-automotive'
        },
    },
]


@pytest.mark.parametrize('method,expected', (
    ('get', '"6441bec00025d84424d9b26e38ff8795"'),
    ('post', None),
    ('patch', None),
    ('put', None),
    ('delete', None),
    ('head', None),
    ('options', None),
))
def test_set_etag_mixin(rf, method, expected):
    class MyView(mixins.SetEtagMixin, TemplateView):

        template_name = 'core/base.html'

        def post(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def patch(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def put(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def delete(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def head(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def options(self, *args, **kwargs):
            return super().get(*args, **kwargs)

    request = getattr(rf, method)('/')
    request.sso_user = None
    view = MyView.as_view()
    response = view(request)

    response.render()
    assert response.get('Etag') == expected


@pytest.mark.parametrize('view_class', mixins.SetEtagMixin.__subclasses__())
def test_cached_views_not_dynamic(rf, settings, view_class):
    # exception will be raised if the views perform http request, which are an
    # indicator that the views rely on dynamic data.
    with requests_mock.mock():
        view = view_class.as_view()
        request = rf.get('/')
        request.LANGUAGE_CODE = 'en-gb'
        # highlights if the view tries to interact with the session, which is
        # also an indicator that the view relies on dynamic data.
        request.session = None
        response = view(request)
        assert response.status_code == 200


def test_cms_language_switcher_one_language(rf):
    class MyView(mixins.CMSLanguageSwitcherMixin, TemplateView):

        template_name = 'core/base.html'

        def get_context_data(self, *args, **kwargs):
            page = {
                'meta': {'languages': [('en-gb', 'English')]}
            }
            return super().get_context_data(page=page, *args, **kwargs)

    request = rf.get('/')
    with translation.override('de'):
        response = MyView.as_view()(request)

    assert response.status_code == 200
    assert response.context_data['language_switcher']['show'] is False


def test_cms_language_switcher_active_language_available(rf):
    class MyView(mixins.CMSLanguageSwitcherMixin, TemplateView):

        template_name = 'core/base.html'

        def get_context_data(self, *args, **kwargs):
            page = {
                'meta': {
                    'languages': [('en-gb', 'English'), ('de', 'German')]
                }
            }
            return super().get_context_data(page=page, *args, **kwargs)

    request = rf.get('/de/')
    with translation.override('de'):
        response = MyView.as_view()(request)

    assert response.status_code == 200
    context = response.context_data['language_switcher']
    assert context['show'] is True


def test_active_view_name(rf):
    class TestView(mixins.ActiveViewNameMixin, TemplateView):
        active_view_name = 'test'
        template_name = 'core/base.html'

    request = rf.get('/')
    response = TestView.as_view()(request)

    assert response.status_code == 200
    assert response.context_data['active_view_name'] == 'test'


def test_child_page_local_slugs_mixin(rf):
    class TestView(mixins.ChildPageLocalSlugs, TemplateView):
        template_name = 'core/base.html'
        subpage_groups = ['sectors']

        def get_context_data(self, *args, **kwargs):
            page = {
                'sectors': test_sectors
            }
            return super().get_context_data(page=page, *args, **kwargs)

    request = rf.get('/')
    response = TestView.as_view()(request)

    updated_sectors = response.context_data['page']['sectors']

    assert response.status_code == 200
    assert updated_sectors[0]['meta']['slug'] == 'aerospace'
    assert updated_sectors[1]['meta']['slug'] == 'automotive'


@patch('core.helpers.cms_client.lookup_by_slug')
def test_get_cms_page_mixin(mock_cms_response, rf):
    class TestView(mixins.GetCMSPageMixin, TemplateView):
        template_name = 'core/base.html'
        slug = 'invest-home-page'

    page = {
        'title': 'the page',
        'meta': {'languages': [('en-gb', 'English'), ('de', 'German')]},
    }

    mock_cms_response.return_value = helpers.create_response(
        status_code=200,
        json_payload=page
    )

    request = rf.get('/')
    response = TestView.as_view()(request)

    assert response.context_data['page'] == page


@patch('core.helpers.cms_client.lookup_by_slug')
def test_get_cms_page_mixin_kwargs_slug(mock_cms_response, rf):
    class TestView(mixins.GetCMSPageMixin, TemplateView):
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

    request = rf.get('/')
    view = TestView.as_view()
    response = view(request, slug='aerospace')

    assert response.context_data['page'] == page


@patch('core.helpers.cms_client.lookup_by_slug')
def test_404_when_cms_language_unavailable(mock_cms_response, rf):
    class TestView(mixins.GetCMSPageMixin, TemplateView):
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

    # fail if this does not return 404
    try:
        assert not view(request, slug='aerospace')
    except Http404 as exception:
        assert True
