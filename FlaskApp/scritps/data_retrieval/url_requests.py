__author__ = 'Kishan'

import sys
from pushbullet import PushBullet
import requests
from FlaskApp.scritps.config import config

from FlaskApp.scritps import data_retrieval

max_attempts = data_retrieval.max_attempts
pb = PushBullet(config.pushbullet_api_key)

def request(url, region='', progress_counter=-1):
    statuscode_not_ok = True
    attempts = 0

    while statuscode_not_ok:
        try:
            data = requests.get(url)
        except:
            print('error')
            pb.push_note("error", "ERROR")
            continue
        if data.ok:
            return data.json()
        else:
            statuscode_not_ok = True
            attempts += 1
            if not progress_counter == -1:
                progress_countdown_error(region, progress_counter,
                                         data, attempts, max_attempts)
            else:
                progress_countdown_error('', '', data, attempts, max_attempts)
                sys.stdout.flush()
        if attempts == max_attempts:
            pb.push_note("error", "ERROR")
            sys.exit('\nError: '
                     + str(data.status_code) + ': '
                     + data.json()['status']['message'])


def progress_countdown_error(region, progress_counter, data, attempts, max_attempts):
    sys.stdout.write('\rProgress Countdown: ' + region.upper() + ' ' +
                     str(progress_counter) + '\t\t' + 'Http status code: ' +
                     str(data.status_code) + '\tRetry attempt...' +
                     str(attempts) + '/' + str(max_attempts))
    sys.stdout.flush()
