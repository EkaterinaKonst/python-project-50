import json
import yaml
from gendiff.formats.set_formatter import set_formatter


def file_opener(file):
    if file.endswith('.json'):
        return json.load(open(file))
    elif file.endswith('.yaml') or file.endswith('.yml'):
        return yaml.safe_load(open(file, 'r'))
    else:
        raise ValueError('Invalid format')


# flake8: noqa: C901
def create_diff(dict1, dict2):
    result = []
    keys = sorted(dict1.keys() | dict2.keys())

    for key in keys:
        node = {'name': key}
        if key not in dict1:
            node['status'] = 'added'
            node['data'] = dict2[key]
        elif key not in dict2:
            node['status'] = 'deleted'
            node['data'] = dict1[key]
        elif type(dict1[key]) is dict and type(dict2[key]) is dict:
            node['status'] = 'nested'
            node['children'] = create_diff(dict1[key], dict2[key])
        elif dict1[key] == dict2[key]:
            node['status'] = 'not changed'
            node['data'] = dict1[key]
        else:
            node['status'] = 'changed'
            node['old_value'] = dict1[key]
            node['new_value'] = dict2[key]
        result.append(node)

    return result


def generate_diff(file1, file2, formatter='stylish'):
    file1 = file_opener(file1)
    file2 = file_opener(file2)
    diff = create_diff(file1, file2)
    return set_formatter(diff, formatter)
