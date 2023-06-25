import json
import yaml
from pathlib import Path


def parser(data, format):
    if format == 'json':
        return json.loads(data)
    elif format == 'yaml' or format == 'yml':
        return yaml.safe_load(data)
    else:
        raise ValueError('Invalid format')


def get_data(path):
    with open(path, "r") as data:
        return parser(data.read(), Path(path).suffix[1:])
