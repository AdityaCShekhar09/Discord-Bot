import json
from pathlib import Path


def get_path():
    cwd = Path(__file__).parents[1]
    cwd = str(cwd)
    return cwd


def read_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def write_json(data,filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
