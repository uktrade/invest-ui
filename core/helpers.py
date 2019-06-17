from django.utils import translation
import requests


def create_response(status_code=200, json_payload=None):
    response = requests.Response()
    response.status_code = status_code
    response.json = lambda: json_payload or {}
    return response


def get_language_from_prefix(path):
    language_codes = translation.trans_real.get_languages()
    prefix = slash_split(path)
    if prefix in language_codes:
        return prefix
    else:
        return 'en-gb'


def slash_split(string):
    if string.count("/") == 1:
        return string.split("/")[0]
    else:
        return "".join(string.split("/", 2)[:2])


def get_untranslated_url(path):
    current_language = get_language_from_prefix(path)
    if current_language == 'en-gb':
        untranslated_url = path
    else:
        untranslated_url = path.replace('/' + current_language + '/', '/')
    return untranslated_url


def count_data_with_field(list_of_data, field_1, field_2, field_3):
    filtered_list = [item for item in list_of_data if
                     item[field_1]
                     and item[field_2]
                     and item[field_3]]
    return len(filtered_list)
