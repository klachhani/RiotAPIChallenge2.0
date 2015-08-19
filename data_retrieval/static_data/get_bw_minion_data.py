__author__ = 'Kishan'

from data_retrieval import url_requests
from config import config
from data_retrieval import static_data


def get_minions_by_id(region = 'euw'):
    minions_by_id = {}
    url = 'https://global.api.pvp.net/api/lol/static-data/'+ region \
          + '/v1.2/item?locale=en_US&api_key=' + config.riot_api_key
    data = url_requests.request(url, max_attempts)['data']

    for key, value in data.items():
        if 'group' in value and value['group'].startswith('BWMerc1'):
            minions_by_id[value['id']] = {'name' : value['name']}

    static_data.write_json(minions_by_id, 'minions_by_id.json')


def get_minions_by_name(region = 'euw'):
    minions_ny_name =  dict(zip(get_minions_by_id(region).values(),
                    get_minions_by_id(region).keys()))

    static_data.write_json(minions_ny_name, 'minions_by_name.json')



def get_minion_upgrades_by_id(region = 'euw'):
    upgrades_by_id = {}
    url = 'https://global.api.pvp.net/api/lol/static-data/'+ region \
          + '/v1.2/item?locale=en_US&api_key=' + config.riot_api_key
    data = url_requests.request(url, max_attempts)['data']

    for key, value in data.items():
        if 'group' in value and value['group'].startswith('BWMerc') \
                and not value['group'].startswith('BWMerc1'):
            upgrades_by_id[value['id']] = {'name' : value['name']}

    static_data.write_json(upgrades_by_id, 'upgrades_by_id.json')


def get_minion_upgrades_by_name(region = 'euw'):
    upgrades_by_name = dict(zip(get_minion_upgrades_by_id(region).values(),
                    get_minion_upgrades_by_id(region).keys()))

    static_data.write_json(upgrades_by_name, 'upgrades_by_name.json')
