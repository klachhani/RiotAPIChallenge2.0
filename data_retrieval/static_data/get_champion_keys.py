__author__ = 'Kishan'

import requests
import config.config as config

def get_champion_key_by_id(region):
    return requests.get('https://global.api.pvp.net/api/lol/static-data/'
                              + region + '/v1.2/champion?champData=all&api_key='
                              + config.riot_api_key).json()['keys']