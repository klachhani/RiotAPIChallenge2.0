__author__ = 'Kishan'

from FlaskApp.scripts.data_retrieval import url_requests
from FlaskApp.scripts.config import config
from FlaskApp.scripts.data_retrieval.static_data import static_io


def get_minions_by_id(region='euw'):
    minions_by_id = {}
    url = 'https://global.api.pvp.net/api/lol/static-data/' + region \
          + '/v1.2/item?locale=en_US&api_key=' + config.riot_api_key
    data = url_requests.request(url)['data']

    for key, value in data.items():
        if 'group' in value and value['group'].startswith('BWMerc1'):
            minions_by_id[value['id']] = value['name']

    static_io.write_json(minions_by_id, 'minions_by_id.json')


def get_minion_upgrades_by_id(region='euw'):
    upgrades_by_id = {}
    url = 'https://global.api.pvp.net/api/lol/static-data/' + region \
          + '/v1.2/item?locale=en_US&api_key=' + config.riot_api_key
    data = url_requests.request(url)['data']

    for key, value in data.items():
        if 'group' in value and value['group'].startswith('BWMerc') \
                and not value['group'].startswith('BWMerc1'):
            upgrades_by_id[value['id']] = value['name']

    static_io.write_json(upgrades_by_id, 'upgrades_by_id.json')


def main():
    get_minions_by_id()
    get_minion_upgrades_by_id()


if __name__ == '__main__':
    main()
