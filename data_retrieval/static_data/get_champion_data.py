__author__ = 'Kishan'

import requests
import config.config as config
import data_retrieval.url_requests as url_requests

def get_champion_by_id(region):
    url = 'https://global.api.pvp.net/api/lol/static-data/'\
          + region + '/v1.2/champion?locale=en_US&champData=all&api_key='\
          + config.riot_api_key

    champ_data = url_requests.request(url, 15)
    return champ_data['keys']


def get_champion_by_key(region):
    return dict(zip(get_champion_by_id(region).values(),
                    get_champion_by_id(region).keys()))