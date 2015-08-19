__author__ = 'Kishan'

from data_retrieval import url_requests
from config import config
from data_retrieval import static_data

max_attempts = static_data.max_attempts

def get_minions_by_id(region):
    dict = {}
    url = 'https://global.api.pvp.net/api/lol/static-data/'+ region \
          + '/v1.2/item?locale=en_US&api_key=' + config.riot_api_key
    data = url_requests.request(url, max_attempts)['data']

    for key, value in data.items():
        if 'group' in value and value['group'].startswith('BWMerc1'):
            dict[value['id']] = {'name' : value['name']}
    return dict


def get_minions_by_name(region):
    return dict(zip(get_minions_by_id(region).values(),
                    get_minions_by_id(region).keys()))


def get_minion_upgrades_by_id(region):
    dict = {}
    url = 'https://global.api.pvp.net/api/lol/static-data/'+ region \
          + '/v1.2/item?locale=en_US&api_key=' + config.riot_api_key
    data = url_requests.request(url, max_attempts)['data']

    for key, value in data.items():
        if 'group' in value and value['group'].startswith('BWMerc') \
                and not value['group'].startswith('BWMerc1'):
            dict[value['id']] = {'name' : value['name']}
    return dict


def get_minion_upgrades_by_name(region):
    return dict(zip(get_minion_upgrades_by_id(region).values(),
                    get_minion_upgrades_by_id(region).keys()))