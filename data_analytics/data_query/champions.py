__author__ = 'Kishan'

from data_analytics.data_query import io as query_io
from data_retrieval.static_data import io as static_io
from data_retrieval import static_data
from data_retrieval.match_data import get_match_data


def run_query(regions = get_match_data.get_match_regions(), tiers = static_data.highest_achieved_season_tier):
    champions = static_io.read_json('champions_by_id.json')

    data = query_io.read_json('champions.json')

    result = {}

    create_query_result_dict(result, regions, tiers, champions)
    query_champions_json(result, data, regions, tiers, champions)
    calculate_extras(result)

    winrate = []
    pickrate = []
    picks = []
    for key, value in result['champion'].items():
        winrate.append([key, value['key'], value['winrate']])
        pickrate.append([key, value['key'], value['pickrate'], value['won'] + value['lost']])
    winrate = sorted(winrate, key=lambda x: x[1], reverse=False)
    winrate = sorted(winrate, key=lambda x: x[2], reverse=True)
    pickrate = sorted(pickrate, key=lambda x: x[1], reverse=False)
    pickrate = sorted(pickrate, key=lambda x: x[2], reverse=True)

    result = {'winrate': winrate, 'pickrate': pickrate}
    return result

# champions[region][tier][champion][won: int, lost: int, key: string]
def query_champions_json(result, data, regions, tiers, champions):
    region = (r for r in data.keys() if r in regions)
    for r in region:
        tier = (t for t in data[r].keys() if t in tiers)
        for t in tier:
            champion = (c for c in data[r][t].keys() if c in champions)
            for c in champion:
                result['champion'][c]['won'] += data[r][t][c]['won']
                result['champion'][c]['lost'] += data[r][t][c]['lost']


def create_query_result_dict(result, regions, tiers, champions):
    result['region'] = regions
    result['tier'] = tiers
    result['champion'] = {}
    for c in champions.keys():
        result['champion'][c] = {'key': champions[c]}
        result['champion'][c]['won'] = 0
        result['champion'][c]['lost'] = 0


def calculate_extras(result):
    total_picks = 0
    for key, value in result['champion'].items():
        total_picks += value['won'] + value['lost']
        champ_picks = value['won'] + value['lost']
        value['winrate'] = ("%.3f" % (100 * (value['won'] / champ_picks)) if not champ_picks == 0 else '0')

    for key, value in result['champion'].items():
        champ_picks = value['won'] + value['lost']
        value['pickrate'] = ("%.3f" % (100 * (champ_picks / total_picks)) if not champ_picks == 0 else '0')

    result['totalpicks'] = total_picks


if __name__ == '__main__':
    a = run_query(tiers=['CHALLENGER'])
    print(a['winrate'])
    print(a['pickrate'])
