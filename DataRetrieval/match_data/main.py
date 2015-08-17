__author__ = 'Kishan'

import os
import sys
import json
import requests
import dataretrieval
import config.config as config


match_id_directory = config.match_ids_directory
match_data_directory = config.match_data_directory
progress_counter = int

def main():
    global progress_counter
    regions = get_match_regions()
    match_ids = get_match_ids([os.path.join(
        config.match_ids_directory, x.upper() + '.json')
                               for x in regions])

    print('\n\nGetting Match Data...\n')
    for i in range(len(match_ids)):
        progress_counter = len(match_ids[i])
        for j in range(len(match_ids[i])):
            if file_exists(regions[i], match_ids[i][j]):
                progress_counter -= 1
                continue
            match_data = get_match_data(regions[i], match_ids[i][j], progress_counter)
            if match_data == 0:

                return
            else:
                progress_counter -= 1
                write_match_data(match_data, regions[i], match_ids[i][j])
            progress_countdown(progress_counter, regions[i])


def get_match_regions():
    regions = []

    for f in os.listdir(match_id_directory):
        if f.endswith('.json'):
            regions.append((f[:-5]).lower())
    regions.sort()

    return regions


def get_match_ids(match_id_files):
    match_ids = []

    for f in match_id_files:
        match_ids.append(json.load(open(f)))

    return match_ids


def file_exists(region, match_id):
    return os.path.isfile(os.path.join(os.path.join
                                       (match_data_directory, region),
                                       str(match_id) + '.json'))


def write_match_data(match_data, region, match_id):
    with open(os.path.join(os.path.join(match_data_directory, region.upper()),
                           str(match_id) + '.json'), 'w') as outfile:
        json.dump(match_data, outfile)


def get_match_data(region, match_id, progress_coutner):

    statuscode_not_ok = True
    max_attempts = 15
    attempts = 0
    url = url_builder(region, match_id, '/v2.2/match/')

    while statuscode_not_ok:
        data = requests.get(url)
        if data.ok:
            return data.json()
        else:
            statuscode_not_ok = True
            attempts += 1
            progress_countdown_error(region, progress_counter,
                                     data, attempts, max_attempts)
        if attempts == max_attempts:
            print('\nAborting')
            return 0


def url_builder(region, match_id, api_request):
    https = 'https://'
    riot_api = '.api.pvp.net/api/lol/'
    timeline = 'true'

    return (https + region + riot_api + region + api_request +
            str(match_id) + '?includeTimeline=' + timeline + '&api_key=' +
            config.riot_api_key)


def progress_countdown(progress_counter, region):
    sys.stdout.write('\rProgress Countdown: ' + region.upper() +
                             ' ' +  str(progress_counter))
    sys.stdout.flush()


def progress_countdown_error(region, progress_counter, data, attempts, max_attempts):
    sys.stdout.write('\rProgress Countdown: ' + region.upper() + ' ' +
                                 str(progress_counter) + '\t\t' + 'Http status code: ' +
                                 str(data.status_code) + '\tRetry attempt...' +
                                 str(attempts) + '/' + str(max_attempts))
    sys.stdout.flush()


if __name__ == '__main__':
    main()