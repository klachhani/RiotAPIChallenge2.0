__author__ = 'Kishan'

from FlaskApp.FlaskApp.scritps.config import config
from FlaskApp.FlaskApp.scritps.data_retrieval.match_data import get_match_data
import os
import json
import sys

match_data_directory = config.match_data_directory
regions = get_match_data.get_match_regions()


def progress_countdown(progress_counter, region):
    sys.stdout.write('\rProgress Countdown: ' + region.upper() +
                     ' ' + str(progress_counter))
    sys.stdout.flush()


for r in regions:
    match_data_directory = os.path.join(config.match_data_directory, r.upper())
    matches = os.listdir(match_data_directory)
    progress_counter = len(matches)
    for m in matches:
        if not m.endswith('.json'):
            continue
        with open(os.path.join(match_data_directory, str(m)), 'r') as f:
            try:
                json.load(f)
            except ValueError:
                progress_counter -= 1
                print('\nValue Error: ' + str(m) + '\n')
                continue
        progress_counter -= 1
        progress_countdown(progress_counter, r)
