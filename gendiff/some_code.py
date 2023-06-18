import json
import yaml
import itertools


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


def get_string(data, indent):
    if type(data) is dict:
        indent += '    '
        result = '{\n'
        for key in data.keys():
            value = get_string(data[key], indent)
            result += f'{indent}  {key}: {value}\n'
        result += indent[:-2] + '}'
    elif data is None:
        result = 'null'
    elif type(data) is bool:
        result = str(data).lower()
    else:
        result = str(data)
    return result


# flake8: noqa: C901
def stylish(diff_list, level=0):
    result = '{\n'
    indent = '  '

    for _ in range(level):
        indent += '    '

    diff_list.sort(key=lambda x: x['name'])

    for node in diff_list:
        if node['status'] == 'nested':
            data = stylish(node['children'], level + 1)
            result += f"{indent}  {node['name']}: {data}\n"
        elif node['status'] == 'not changed':
            data = get_string(node['data'], indent)
            result += f"{indent}  {node['name']}: {data}\n"
        elif node['status'] == 'added':
            data = get_string(node['data'], indent)
            result += f"{indent}+ {node['name']}: {data}\n"
        elif node['status'] == 'deleted':
            data = get_string(node['data'], indent)
            result += f"{indent}- {node['name']}: {data}\n"
        else:
            data = get_string(node['old_value'], indent)
            result += f"{indent}- {node['name']}: {data}\n"
            data = get_string(node['new_value'], indent)
            result += f"{indent}+ {node['name']}: {data}\n"
    result += indent[:-2] + '}'

    return result


def generate_diff(file1, file2, formatter='stylish'):
    file1 = file_opener(file1)
    file2 = file_opener(file2)
    diff = create_diff(file1, file2)
    if formatter == 'stylish':
        return stylish(diff)
