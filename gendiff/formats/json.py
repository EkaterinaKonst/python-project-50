import json


def get_json_format(diff_list):
    return json.dumps(diff_list, indent=4)
