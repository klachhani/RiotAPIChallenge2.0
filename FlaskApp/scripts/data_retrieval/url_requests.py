__author__ = 'Kishan'

import sys
import requests
from FlaskApp.scripts import data_retrieval

max_attempts = data_retrieval.max_attempts


# get json from url
def request(url, region='', progress_counter=-1):
    statuscode_not_ok = True
    attempts = 0

    # loop until http status code is ok or until max attempts is reached
    while statuscode_not_ok:
        try:
            data = requests.get(url)
        except:
            # retry on request error, does no contribute to attempts
            print('error')
            continue
        if data.ok:
            # return json if status is ok
            return data.json()
        else:
            statuscode_not_ok = True
            attempts += 1
            # print progress
            if not progress_counter == -1:
                progress_countdown_error(region, progress_counter,
                                         data, attempts, max_attempts)
            else:
                progress_countdown_error('', '', data, attempts, max_attempts)
                sys.stdout.flush()
        # end loop if max attempts is reached and print status code
        if attempts == max_attempts:
            sys.exit('\nError: '
                     + str(data.status_code) + ': '
                     + data.json()['status']['message'])


# progress countdown method which also outputs status code errors and rety attempts
def progress_countdown_error(region, progress_counter, data, attempts, max_attempts):
    sys.stdout.write('\rProgress Countdown: ' + region.upper() + ' ' +
                     str(progress_counter) + '\t\t' + 'Http status code: ' +
                     str(data.status_code) + '\tRetry attempt...' +
                     str(attempts) + '/' + str(max_attempts))
    sys.stdout.flush()
