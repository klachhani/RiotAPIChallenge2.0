__author__ = 'Kishan'

import os
import json
import sys


def write_json(dict, filename):
    path = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)
    with open(filename, 'w') as outfile:
        json.dump(dict, outfile)


def progress_countdown(progress_counter, region):
    sys.stdout.write('\rPopulating dict...' + region.upper() +
                     ' ' + str(progress_counter))
    sys.stdout.flush()
