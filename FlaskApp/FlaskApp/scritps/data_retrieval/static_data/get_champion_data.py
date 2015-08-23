__author__ = 'Kishan'

from FlaskApp.FlaskApp.scritps.config import config
from FlaskApp.FlaskApp.scritps.data_retrieval import url_requests
from FlaskApp.FlaskApp.scritps.data_retrieval.static_data import io


def get_champion_by_id(region='euw'):
    url = 'https://global.api.pvp.net/api/lol/static-data/' \
          + region + '/v1.2/champion?locale=en_US&champData=all&api_key=' \
          + config.riot_api_key

    champion_by_id = url_requests.request(url)['keys']
    io.write_json(champion_by_id, 'champions_by_id.json')


def main():
    get_champion_by_id()


if __name__ == '__main__':
    main()
