import pytest
from django.utils import translation

from invest.templatetags.invest_tags import title_from_heading


@pytest.mark.parametrize('value, expected_result', [
    ('title: heading', 'title'),
    ('title', 'title')
])
def test_title_from_heading(value, expected_result):
    assert title_from_heading(value) == expected_result


def test_title_from_heading_bidi_language():
    translation.activate('ar')
    assert title_from_heading('heading: title') == 'title'
