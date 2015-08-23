__author__ = 'Kishan'

from data_analytics.data_query import io as query_io
from data_retrieval.static_data import io as static_io
from data_retrieval import static_data
from data_retrieval.match_data import get_match_data


def run_query(regions = get_match_data.get_match_regions(), tiers = static_data.highest_achieved_season_tier):
    champions = static_io.read_json('champions_by_id.json')

    data = query_io.read_json('champions.json')

    result = {}

    create_empty_result_dict(result, champions)
    query_champions_json(result, data, regions, tiers, champions)
    calculate_extras(result)

    winrate = []
    pickrate = []
    for key, value in result.items():
        winrate.append([key, value['key'], value['winrate']])
        pickrate.append([key, value['key'], value['pickrate'], value['won'] + value['lost']])
    winrate = sorted(sorted(winrate, key=lambda x: x[1], reverse=False), key=lambda x: x[2], reverse=True)
    pickrate = sorted(sorted(pickrate, key=lambda x: x[1], reverse=False), key=lambda x: x[2], reverse=True)

    result = {'winrate': winrate, 'pickrate': pickrate}
    return result

def query_champions_json(result, data, regions, tiers, champions):
    region = (r for r in data.keys() if r in regions)
    for r in region:
        tier = (t for t in data[r].keys() if t in tiers)
        for t in tier:
            champion = (c for c in data[r][t].keys() if c in champions)
            for c in champion:
                result[c]['won'] += data[r][t][c]['won']
                result[c]['lost'] += data[r][t][c]['lost']


def create_empty_result_dict(result, champions):
    for c in champions.keys():
        result[c] = {'key': champions[c], 'won' : 0, 'lost' : 0}


def calculate_extras(result):
    total_picks = 0
    for key, value in result.items():
        total_picks += value['won'] + value['lost']
        champ_picks = value['won'] + value['lost']
        value['winrate'] = float("%.3f" % (100 * (value['won'] / champ_picks)) if not champ_picks == 0 else '0')

    for key, value in result.items():
        champ_picks = value['won'] + value['lost']
        value['pickrate'] = float("%.3f" % (100 * (champ_picks / total_picks)) if not total_picks == 0 else '0')

if __name__ == '__main__':
    a = run_query()
    print(a['winrate'])
    print(a['pickrate'])
