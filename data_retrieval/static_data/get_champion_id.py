__author__ = 'Kushil'
import requests
import config.config as config

def get_champion_key_by_id(region):
    return requests.get('https://global.api.pvp.net/api/lol/static-data/'
                              + str(region) + '/v1.2/champion?dataById=true&api_key='

                              + config.riot_api_key).json()['data'].keys()


