__author__ = 'Kishan'

from FlaskApp.scritps.config import config
from FlaskApp.scritps.data_retrieval import url_requests
from FlaskApp.scritps.data_retrieval.static_data import static_io


def get_champion_by_id(region='euw'):
    url = 'https://global.api.pvp.net/api/lol/static-data/' \
          + region + '/v1.2/champion?locale=en_US&api_key=' \
          + config.riot_api_key

    data = url_requests.request(url)['data']
    champion_by_id = {}
    print(data)
    for champ in data.values():
        champion_by_id[champ['id']] = {'key' :champ['key'], 'name' : champ['name']}
    static_io.write_json(champion_by_id, 'champions_by_id.json')


def main():
    get_champion_by_id()


if __name__ == '__main__':
    main()
