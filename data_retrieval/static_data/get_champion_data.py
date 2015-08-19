__author__ = 'Kishan'

from config import config
from data_retrieval import url_requests
from  data_retrieval import static_data

max_attempts = static_data.max_attempts


def get_champion_by_id(region = 'euw'):
    url = 'https://global.api.pvp.net/api/lol/static-data/'\
          + region + '/v1.2/champion?locale=en_US&champData=all&api_key='\
          + config.riot_api_key

    champion_by_id = url_requests.request(url, max_attempts)['keys']
    static_data.write_json(champion_by_id, 'champion_by_id.json')


def get_champion_by_key(region = 'euw'):
    champion_by_name = dict(zip(get_champion_by_id(region).values(),
                    get_champion_by_id(region).keys()))

    static_data.write_json(champion_by_name, 'champion_by_name.json')
