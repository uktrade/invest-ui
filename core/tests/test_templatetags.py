import pytest
from django.template import Context, Template
from django.utils import translation
from core.templatetags.cms_tags import (
    help_sections_to_list,
    subsections_to_list,
    title_from_heading
)

from bs4 import BeautifulSoup


def test_add_anchors():
    template = Template(
        '{% load add_anchors from cms_tags %}'
        '{{ html|add_anchors|safe }}'
    )

    context = Context({
        'html': '<br/><h2>Title one</h2><h2>Title two</h2><br/>'
    })
    html = template.render(context)

    assert html == (
        '<br/>'
        '<h2 id="title-one-section">Title one</h2>'
        '<h2 id="title-two-section">Title two</h2>'
        '<br/>'
    )


def test_table_of_contents():
    template = Template(
        '{% load table_of_contents from cms_tags %}'
        '{% for anchor, label in html|table_of_contents %}'
        '    <a href="#{{ anchor }}">{{ label }}</a>'
        '{% endfor %}'
    )

    context = Context({
        'html': '<br/><h2>Title one</h2><h2>Title two</h2><br/>'
    })
    html = template.render(context)

    assert html == (
        '    <a href="#title-one-section">Title one</a>'
        '    <a href="#title-two-section">Title two</a>'
    )


def test_first_paragraph():
    template = Template(
        '{% load first_paragraph from cms_tags %}'
        '{{ html|first_paragraph|safe }}'

    )
    context = Context({
        'html': '<p>The first paragraph</p><p></p>'
    })
    html = template.render(context)

    assert html == '<p>The first paragraph</p>'


def test_first_image():
    template = Template(
        '{% load first_image from cms_tags %}'
        '{{ html|first_image|safe }}'

    )
    context = Context({
        'html': (
            '<p>The first paragraph</p>'
            '<p><img src="path/to/image" height="100" width="50"/></p>'
        )
    })
    html = template.render(context)

    assert html == '<img src="path/to/image" width="50"/>'


def test_first_image_empty():
    template = Template(
        '{% load first_image from cms_tags %}'
        '{{ html|first_image|safe }}'

    )
    context = Context({
        'html': (
            '<p>The first paragraph</p>'
            '<p></p>'
        )
    })
    html = template.render(context)

    assert html == ''


def test_grouper():
    template = Template(
        '{% load grouper from cms_tags %}'
        '{% for chunk in the_list|grouper:3 %}'
        '<ul>'
        '    {% for item in chunk %}'
        '    <li>{{ item }}</li>'
        '    {% endfor %}'
        '</ul>'
        '{% endfor %}'

    )
    context = Context({
        'the_list': range(1, 10)
    })
    html = template.render(context)

    assert html == (
        '<ul>'
        '        <li>1</li>'
        '        <li>2</li>'
        '        <li>3</li>'
        '    </ul>'
        '<ul>'
        '        <li>4</li>'
        '        <li>5</li>'
        '        <li>6</li>'
        '    </ul>'
        '<ul>'
        '        <li>7</li>'
        '        <li>8</li>'
        '        <li>9</li>'
        '    </ul>'
    )


def test_grouper_remainder():
    template = Template(
        '{% load grouper from cms_tags %}'
        '{% for chunk in the_list|grouper:3 %}'
        '<ul>'
        '    {% for item in chunk %}'
        '    <li>{{ item }}</li>'
        '    {% endfor %}'
        '</ul>'
        '{% endfor %}'

    )
    context = Context({
        'the_list': range(1, 6)
    })
    html = template.render(context)

    assert html == (
        '<ul>'
        '        <li>1</li>'
        '        <li>2</li>'
        '        <li>3</li>'
        '    </ul>'
        '<ul>'
        '        <li>4</li>'
        '        <li>5</li>'
        '    </ul>'
    )


def test_add_export_elements_classes():
    template = Template(
        '{% load add_export_elements_classes from cms_tags %}'
        '{{ html|add_export_elements_classes|safe }}'

    )
    context = Context({
        'html': (
            '<br/>'
            '<h2>Title one</h2>'
            '<h3>Title two</h3>'
            '<ul>List one</ul>'
            '<ol>List two</ol>'
        )
    })
    html = template.render(context)

    assert html == (
        '<br/>'
        '<h2 class="heading-large">Title one</h2>'
        '<h3 class="heading-medium">Title two</h3>'
        '<ul class="list list-bullet">List one</ul>'
        '<ol class="list list-number">List two</ol>'
    )


def test_add_href_target(rf):
    request = rf.get('/', HTTP_HOST='www.example.com')
    template = Template(
        '{% load add_href_target from cms_tags %}'
        '{{ html|add_href_target:request|safe }}'

    )
    context = Context({
        'request': request,
        'html': (
            '<a href="http://www.google.com"></a>'
            '<a href="https://www.google.com"></a>'
            '<a href="http://www.example.com"></a>'
            '<a href="https://www.example.com"></a>'
        )
    })
    html = template.render(context)

    assert html == (
        '<a href="http://www.google.com" target="_blank"></a>'
        '<a href="https://www.google.com" target="_blank"></a>'
        '<a href="http://www.example.com"></a>'
        '<a href="https://www.example.com"></a>'
    )


def test_filter_by_active_language(rf):
    request = rf.get('/', HTTP_HOST='www.example.com')
    translation.activate('fr')
    template = Template(
        '{% load filter_by_active_language from cms_tags %}'
        '{% for sector in sectors|filter_by_active_language %}'
        '<h1>{{ sector.title }}</h1>'
        '{% endfor %}'
    )

    test_sectors = [
        {
            'title': 'Aerospace',
            'meta': {
                'slug': 'invest-aerospace',
                'languages': [
                    ['en-gb', 'English'],
                ],
            },
        },
        {
            'title': 'Automotive',
            'meta': {
                'slug': 'invest-automotive',
                'languages': [
                    ['en-gb', 'English'],
                    ['fr', 'Français'],
                ],
            },
        },
    ]

    context = Context({
        'request': request,
        'sectors': test_sectors
    })

    filtered = template.render(context)
    soup = BeautifulSoup(filtered, 'html.parser')

    assert len(soup.find_all('h1')) == 1
    assert soup.find('h1').string == 'Automotive'


def test_how_we_help_sections_to_list():
    page = {
        'how_we_help_text_one': 'Text one',
        'how_we_help_icon_one': {
            'url': 'icon.png', 'width': 128, 'height': 128},
        'how_we_help_text_two': 'Text two',
        'how_we_help_icon_two': {
            'url': 'icon.png', 'width': 128, 'height': 128},
        'how_we_help_text_three': 'Text three',
        'how_we_help_icon_three': {
            'url': 'icon.png', 'width': 128, 'height': 128},
        'how_we_help_text_four': 'Text four',
        'how_we_help_icon_four': {
            'url': 'icon.png', 'width': 128, 'height': 128},
        'how_we_help_text_five': 'Text five',
        'how_we_help_icon_five': {
            'url': 'icon.png', 'width': 128, 'height': 128},
        'how_we_help_text_six': 'Contact us',
        }
    exp = [
        {
            'text': 'Text one',
            'icon': {'url': 'icon.png', 'width': 128, 'height': 128}
        },
        {
            'text': 'Text two',
            'icon': {'url': 'icon.png', 'width': 128, 'height': 128}
        },
        {
            'text': 'Text three',
            'icon': {'url': 'icon.png', 'width': 128, 'height': 128}
        },
        {
            'text': 'Text four',
            'icon': {'url': 'icon.png', 'width': 128, 'height': 128}
        },
        {
            'text': 'Text five',
            'icon': {'url': 'icon.png', 'width': 128, 'height': 128}
        },
        {'text': 'Contact us'},
    ]
    assert help_sections_to_list(page) == exp


def test_subsections_to_list():
    page = {
        'subsection_title_one': 'Title 1',
        'subsection_content_one': '<p>Content 1.</p>',
        'subsection_map_one': None,
        'subsection_title_two': 'Title 2',
        'subsection_content_two': '<p>Content 2.</p>',
        'subsection_map_two': {
            'url': 'map.png', 'width': 1000, 'height': 1290},
        'subsection_title_three': 'Title 3',
        'subsection_content_three': '<p>Content 3.</p>',
        'subsection_map_three': None,
        'subsection_title_four': 'Title 4',
        'subsection_content_four': '<p>Content 4.</p>',
        'subsection_map_four': None,
        'subsection_title_five': '',
        'subsection_content_five': '',
        'subsection_map_five': None,
        'subsection_title_six': '',
        'subsection_content_six': '',
        'subsection_map_six': None,
        'subsection_title_seven': '',
        'subsection_content_seven': '',
        'subsection_map_seven': None,
        }
    exp = [
        {'content': '<p>Content 1.</p>', 'title': 'Title 1', 'map': None},
        {'content': '<p>Content 2.</p>', 'title': 'Title 2',
            'map': {'url': 'map.png', 'width': 1000, 'height': 1290}},
        {'content': '<p>Content 3.</p>', 'title': 'Title 3', 'map': None},
        {'content': '<p>Content 4.</p>', 'title': 'Title 4', 'map': None},
        {'content': '', 'map': None, 'title': ''},
        {'content': '', 'map': None, 'title': ''},
        {'content': '', 'map': None, 'title': ''},
    ]
    assert subsections_to_list(page) == exp


@pytest.mark.parametrize('value, expected_result', [
    ('title: heading', 'title'),
    ('アグリテック：貴社のビジネスを英国で発展させよう', 'アグリテック'),
    ('title', 'title')
])
def test_title_from_heading(value, expected_result):
    assert title_from_heading(value) == expected_result
