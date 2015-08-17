__author__ = 'Kishan'

import requests
import sys
from socket import gaierror
from pushbullet import Pushbullet
import config.config as config

pushbullet_api_key = config.pushbullet_api_key

if not pushbullet_api_key == '':
    pb = Pushbullet(pushbullet_api_key)



def request(url, max_attempts, region, progress_counter = -1):
    statuscode_not_ok = True
    attempts = 0

    while statuscode_not_ok:
        try:
            data = requests.get(url)
        except gaierror:
            print('\n')
            if not pushbullet_api_key == '':
                pb.push_note('Connection error', gaierror)
            sys.exit(gaierror)
        if data.ok:
            return data.json()
        else:
            statuscode_not_ok = True
            attempts += 1
            if not progress_counter == -1:
                progress_countdown_error(region, progress_counter,
                                         data, attempts, max_attempts)
        if attempts == max_attempts:
            print('\n')
            err_msg = 'Error: ' + str(data.status_code) + ': ' \
                      + data.json()['status']['message']
            if not pushbullet_api_key == '':
                pb.push_note('Reached max attempts', err_msg + '\n'
                             + progress_counter + ' Remaning for '
                             + region.upper())
            sys.exit('Error: '
                     + str(data.status_code) + ': '
                     + data.json()['status']['message'])


def progress_countdown_error(region, progress_counter, data, attempts, max_attempts):
    sys.stdout.write('\rProgress Countdown: ' + region.upper() + ' ' +
                                 str(progress_counter) + '\t\t' + 'Http status code: ' +
                                 str(data.status_code) + '\tRetry attempt...' +
                                 str(attempts) + '/' + str(max_attempts))