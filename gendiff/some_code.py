import json
import yaml
from os.path import splitext
import itertools


# flake8: noqa: C901
def build_diff(parced_data1: dict, parced_data2: dict):
    diff = list()
    sorted_keys = sorted(
        list(set(parced_data1.keys()) | set(parced_data2.keys()))
    )
    for key in sorted_keys:
        if key not in parced_data1:
            diff.append({
                'key': key,
                'operation': 'add',
                'new': parced_data2[key]
            })
        elif key not in parced_data2:
            diff.append({
                'key': key,
                'operation': 'removed',
                'old': parced_data1[key]
            })
        elif isinstance(parced_data1[key], dict) and isinstance(
                parced_data2[key], dict):
            child = build_diff(parced_data1[key], parced_data2[key])
            diff.append({
                'key': key,
                'operation': 'nested',
                'value': child
            })
        elif parced_data1[key] == parced_data2[key]:
            diff.append({
                'key': key,
                'operation': 'same',
                'value': parced_data1[key]
            })
        elif parced_data1[key] != parced_data2[key]:
            diff.append({
                'key': key,
                'operation': 'changed',
                'old': parced_data1[key],
                'new': parced_data2[key]
            })
    return diff


def prepare_data(path_file: str):
    original_format = splitext(path_file)[1][1:]
    if original_format == 'json':
        with open(path_file) as f:
            json_data = json.load(f)
            return json_data
    elif original_format == 'yaml' or original_format == 'yml':
        with open(path_file) as fh:
            yml_data = yaml.load(fh, Loader=yaml.FullLoader)
            return yml_data


def generate_diff(path_file1: str, path_file2: str):
    data1 = prepare_data(path_file1)
    data2 = prepare_data(path_file2)
    tmp_diff = build_diff(data1, data2)
    diff_to_str = ''
    diff_to_str += '{\n'
    for i in tmp_diff:
        if i['operation'] == 'removed':
            diff_to_str += f' - {i["key"]}: {i["old"]}\n'
        elif i['operation'] == 'same':
            diff_to_str += f'   {i["key"]}: {i["value"]}\n'
        elif i['operation'] == 'changed':
            diff_to_str += f' - {i["key"]}: {i["old"]}\n'
            diff_to_str += f' + {i["key"]}: {i["new"]}\n'
        elif i['operation'] == 'add':
            diff_to_str += f' + {i["key"]}: {i["new"]}\n'
    diff_to_str += '}'
    return diff_to_str


def stringify(val, depth):
    """
    transforms values to string and translates bool & None
    values to correct JavaScript names.
    """
    if isinstance(val, bool):
        return 'true' if val else 'false'
    elif val is None:
        return 'null'
    elif type(val) != dict:
        return val
    replacer = ' '
    deep_indent_size = depth + 1
    deep_indent = deep_indent_size * replacer
    current_indent = replacer * depth
    lines = []
    if isinstance(val, dict):
        for key in val:
            lines.append(f'{deep_indent}{key}: {stringify(val.get(key), depth + 1)}')
        result = itertools.chain('{', lines, [current_indent + '}'])
        return '\n'.join(result)


def basic_indent(depth):
    size = depth * 4 - 2
    return ' ' * size


def stylish(path_file1: str, path_file2: str):
    data1 = prepare_data(path_file1)
    data2 = prepare_data(path_file2)
    tmp_diff = build_diff(data1, data2)

    def iter_(lst, depth=0):
        lines = []
        for elem in lst:
            indent = basic_indent(depth)
            key_elem = elem['key']
            if elem['operation'] == 'add':
                new_elem = stringify(elem['new'], depth + 4)
                lines.append(f'{indent}+ {key_elem}: {new_elem}')
            elif elem['operation'] == 'remove':
                removed_elem = stringify(elem['removed'], depth + 4)
                lines.append(f'{indent}- {key_elem}: {removed_elem}')
            elif elem['operation'] == 'same':
                same_elem = stringify(elem['value'], depth + 4)
                lines.append(f'{indent}  {key_elem}: {same_elem}')
            elif elem['operation'] == 'nest':
                children = elem['value']
                inside = iter_(children, depth + 1)
                key_elem_dict = elem['key']
                lines.append(f'{indent}{key_elem_dict}: {inside}')
                depth += 1
        current_indent = ' ' * depth
        result = itertools.chain('{', lines, [current_indent + '}'])
        return '\n'.join(result)
    return iter_(tmp_diff, 1)