from gendiff.formats.json import _json
from gendiff.formats.plain import plain
from gendiff.formats.stylish import stylish


def set_formatter(diff_list, format):
    if format == 'stylish':
        return stylish(diff_list)
    elif format == 'json':
        return _json(diff_list)
    elif format == 'plain':
        return plain(diff_list)
