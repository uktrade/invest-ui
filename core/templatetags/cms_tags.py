import re

from bs4 import BeautifulSoup

from django import template
from django.utils.text import slugify
from django.utils import translation


register = template.Library()


def build_anchor_id(element):
    return slugify(get_label(element) + '-section')


def get_label(element):
    return re.sub(r'^.* \- ', '', element.contents[0])


@register.filter
def add_anchors(value):
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll('h2'):
        element.attrs['id'] = build_anchor_id(element)
    return str(soup)


@register.filter
def table_of_contents(value):
    soup = BeautifulSoup(value, 'html.parser')
    return [
        (build_anchor_id(element), get_label(element))
        for element in soup.findAll('h2')
    ]


@register.filter
def first_paragraph(value):
    soup = BeautifulSoup(value, 'html.parser')
    element = soup.find('p')
    return str(element)


@register.filter
def first_image(value):
    soup = BeautifulSoup(value, 'html.parser')
    element = soup.find('img')
    if not element:
        return ''
    del element['height']
    return element


@register.filter
def grouper(value, n):
    ungrouped = value or []
    return [ungrouped[x:x+n] for x in range(0, len(ungrouped), n)]


@register.filter
def add_export_elements_classes(value):
    soup = BeautifulSoup(value, 'html.parser')
    mapping = [
        ('h2', 'heading-large'),
        ('h3', 'heading-medium'),
        ('ul', 'list list-bullet'),
        ('ol', 'list list-number'),
        ('a', 'link'),
    ]
    for tag_name, class_name in mapping:
        for element in soup.findAll(tag_name):
            element.attrs['class'] = class_name
    return str(soup)


@register.filter
def add_href_target(value, request):
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll('a', attrs={'href': re.compile("^http")}):
        if request.META['HTTP_HOST'] not in element.attrs['href']:
            element.attrs['target'] = '_blank'
    return str(soup)


@register.filter
def filter_by_active_language(pages):
    return [page for page in pages if is_translated_to_current_language(page)]


def is_translated_to_current_language(page):
    active_language = translation.get_language()
    for code, _ in page['meta']['languages']:
        if code == active_language:
            return True
    else:
        return False


@register.filter
def subsections_to_list(page):
    content_types = [
        'title',
        'content',
        'map',
    ]
    return filter_subsections(page, 'subsection_', content_types)


@register.filter
def help_sections_to_list(page):
    content_types = [
        'text',
        'icon',
    ]
    return filter_subsections(page, 'how_we_help_', content_types)


def filter_subsections(page, prefix, content_types):
    suffixes = [
        '_one',
        '_two',
        '_three',
        '_four',
        '_five',
        '_six',
        '_seven',
    ]
    subsections_list = []
    for suffix in suffixes:
        section = {}
        for content_type in content_types:
            original_field = prefix + content_type + suffix
            if original_field in page:
                section[content_type] = page[original_field]
        if section:
            subsections_list.append(section)
    return subsections_list
