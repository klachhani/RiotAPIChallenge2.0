__author__ = 'Kishan'

import data_retrieval.url_requests as url_requests
import data_retrieval.match_data.get_match_data as match_data
import config.config as config

regions = [(match_data.get_match_regions())[0]] #Limit regions?
max_attempts = 15

bw_minions = {}
for r in regions:
    url = 'https://global.api.pvp.net/api/lol/static-data/'+ r \
          + '/v1.2/item?api_key=' + config.riot_api_key
    data = url_requests.request(url, r, max_attempts)['data']
    bw_minions[r] = {}
