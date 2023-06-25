from gendiff.formats.json import get_json_format
from gendiff.formats.plain import get_plain_format
from gendiff.formats.stylish import get_stylish_format


def set_formatter(diff_list, format):
    if format == 'stylish':
        return get_stylish_format(diff_list)
    elif format == 'json':
        return get_json_format(diff_list)
    elif format == 'plain':
        return get_plain_format(diff_list)
