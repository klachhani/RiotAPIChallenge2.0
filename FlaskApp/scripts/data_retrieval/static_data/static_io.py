__author__ = 'Kishan'

import os
import json


# Read and write JSON for static data
def read_json(filename):
    path = os.path.join(os.path.dirname(__file__), r'data')
    file_path = os.path.join(path, filename)
    with open(file_path, 'r') as f:
        return json.load(f)


def write_json(dict, filename):
    path = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)
    with open(filename, 'w') as outfile:
        json.dump(dict, outfile)
