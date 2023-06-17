import json
import yaml
import itertools


def file_opener(file1, file2):
    def inner_(file):
        if file.endswith('.json'):
            file = json.load(open(file))
        elif file.endswith('.yaml') or file.endswith('.yml'):
            file = yaml.safe_load(open(file, 'r'))
        else:
            raise ValueError('Invalid format')
        return file
    file1 = inner_(file1)
    file2 = inner_(file2)
    return file1, file2


#noqa: с901
def diff_seeker(file1, file2):
    diff = list()
    sorted_keys = sorted(list(set(file1.keys()) | set(file2.keys())))
    for key in sorted_keys:
        if key not in file1:
            diff.append(
                {'key': key,
                 'operation': 'add',
                 'new': file2[key]
                 })
        elif key not in file2:
            diff.append(
                {'key': key,
                 'operation': 'remove',
                 'removed': file1[key]})
        elif isinstance(file1[key], dict) and isinstance(file2[key], dict):
            children = diff_seeker(file1[key], file2[key])
            diff.append(
                {'key': key,
                 'operation': 'nest',
                 'value': children})
        elif key in file1 and key in file2 and file1[key] != file2[key]:
            diff.append(
                {'key': key,
                 'operation': 'remove',
                 'removed': file1[key]})
            diff.append(
                {'key': key,
                 'operation': 'add',
                 'new': file2[key]})
        elif key in file1 and key in file2 and file1[key] == file2[key]:
            diff.append(
                {'key': key,
                 'operation': 'same',
                 'value': file1[key]})
    return diff


def stringify(val, depth):
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


#noqa: с901
def stylish(dict1, dict2):
    diff_list = diff_seeker(dict1, dict2)

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
    return iter_(diff_list, 1)


def generate_diff(file1, file2, formatter='stylish'):
    file1, file2 = file_opener(file1, file2)
    if formatter == 'stylish':
        return stylish(file1, file2)
