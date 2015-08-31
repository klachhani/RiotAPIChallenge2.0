__author__ = 'Kishan'

from FlaskApp.scripts.config import config
from FlaskApp.scripts.data_retrieval import url_requests
from FlaskApp.scripts.data_retrieval.static_data import static_io


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


def get_sorted_champions(sort_by):
    champs = static_io.read_json('champions_by_id.json')
    sorted_champions = []
    for id, value in champs.items():
        sorted_champions.append({'id': int(id), 'name': value['name'], 'key': value['key']})
    sorted_champions = sorted(sorted_champions, key=lambda k: k[sort_by])
    return sorted_champions

def main():
    get_champion_by_id()


if __name__ == '__main__':
    main()
