__author__ = 'Kishan'

import requests
import sys
from socket import gaierror
import data_retrieval

max_attempts = data_retrieval.max_attempts


def request(url, region = '', progress_counter = -1):
    statuscode_not_ok = True
    attempts = 0

    while statuscode_not_ok:
        try:
            data = requests.get(url)
        except gaierror:
            print('\n')
            sys.exit(gaierror)
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
            sys.exit('\nError: '
                     + str(data.status_code) + ': '
                     + data.json()['status']['message'])


def progress_countdown_error(region, progress_counter, data, attempts, max_attempts):
    sys.stdout.write('\rProgress Countdown: ' + region.upper() + ' ' +
                                 str(progress_counter) + '\t\t' + 'Http status code: ' +
                                 str(data.status_code) + '\tRetry attempt...' +
                                 str(attempts) + '/' + str(max_attempts))
    sys.stdout.flush()
