import json


def build_diff(parced_data1: dict, parced_data2: dict):# noqa: C901
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
    with open(path_file) as f:
        data = json.load(f)
        return data


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
