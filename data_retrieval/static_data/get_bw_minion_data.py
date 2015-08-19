__author__ = 'Kishan'

from data_retrieval import url_requests
from config import config
from data_retrieval.static_data import io


def get_minions_by_id(region = 'euw'):
    minions_by_id = {}
    url = 'https://global.api.pvp.net/api/lol/static-data/'+ region \
          + '/v1.2/item?locale=en_US&api_key=' + config.riot_api_key
    data = url_requests.request(url)['data']

    for key, value in data.items():
        if 'group' in value and value['group'].startswith('BWMerc1'):
            minions_by_id[value['id']] = value['name']

    io.write_json(minions_by_id, 'minions_by_id.json')
    return minions_by_id


def get_minions_by_name(region = 'euw'):
    minions_by_id = get_minions_by_id(region)
    minions_ny_name =  dict(zip(minions_by_id.values(), minions_by_id.keys()))

    io.write_json(minions_ny_name, 'minions_by_name.json')



def get_minion_upgrades_by_id(region = 'euw'):
    upgrades_by_id = {}
    url = 'https://global.api.pvp.net/api/lol/static-data/'+ region \
          + '/v1.2/item?locale=en_US&api_key=' + config.riot_api_key
    data = url_requests.request(url)['data']

    for key, value in data.items():
        if 'group' in value and value['group'].startswith('BWMerc') \
                and not value['group'].startswith('BWMerc1'):
            upgrades_by_id[value['id']] = value['name']

    io.write_json(upgrades_by_id, 'upgrades_by_id.json')
    return upgrades_by_id


def get_minion_upgrades_by_name(region = 'euw'):
    upgrades_by_id = get_minion_upgrades_by_id(region)

    upgrades_by_name = dict(zip(upgrades_by_id.values(), upgrades_by_id.keys()))

    io.write_json(upgrades_by_name, 'upgrades_by_name.json')

def main():
    get_minions_by_id()
    get_minion_upgrades_by_id()
    get_minions_by_name()
    get_minion_upgrades_by_name()


if __name__ == '__main__':
    main()