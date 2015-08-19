__author__ = 'Kishan'

from data_analytics.data_query import io as query_io
from data_retrieval.static_data import io as static_io
from data_retrieval import static_data
from data_retrieval.match_data import get_match_data


def main():
    regions = ['br']
    tiers = ['GOLD']
    champions = static_io.read_json('champions_by_id.json')

    if len(tiers) == 0: tiers = static_data.highest_achieved_season_tier
    if len(regions) == 0: regions = get_match_data.get_match_regions()

    data = query_io.read_json('champions.json')
    dict = {}

    create_query_result_dict(dict, regions, tiers, champions)
    query_champions_json(dict, data, regions, tiers, champions)
    calculate_extras(dict)

    winrate = []
    pickrate = []
    for key, value in dict['champion'].items():
        winrate.append([key, value['key'], value['winrate']])
        pickrate.append([key, value['key'], value['pickrate']])
    winrate = sorted(winrate,key=lambda x:x[2], reverse=True)
    pickrate = sorted(pickrate,key=lambda x:x[2], reverse=True)

    print(winrate)
    print(pickrate)

    result = {'winrate' : winrate, 'pickrate' : pickrate}
    query_io.write_json(result, 'test.json')



#champions[region][tier][champion][won: int, lost: int, key: string]
def query_champions_json(dict, data, regions, tiers, champions):
    region = (r for r in data.keys() if r in regions)
    for r in region:
        tier = (t for t in data[r].keys() if t in tiers)
        for t in tier:
            champion = (c for c in data[r][t].keys() if c in champions)
            for c in champion:
                dict['champion'][c]['won'] += data[r][t][c]['won']
                dict['champion'][c]['lost'] += data[r][t][c]['lost']


def create_query_result_dict(dict, regions, tiers, champions):
    dict['region'] = regions
    dict['tier'] = tiers
    dict['champion'] = {}
    for c in champions.keys():
        dict['champion'][c] = {'key': champions[c]}
        dict['champion'][c]['won'] = 0
        dict['champion'][c]['lost'] = 0


def calculate_extras(dict):
    total_picks = 0
    for key, value in dict['champion'].items():
        total_picks += value['won'] + value['lost']
        champ_picks = value['won'] + value['lost']
        value['winrate'] = (100 * (value['won']/champ_picks) if not champ_picks == 0 else 0)

    for key, value in dict['champion'].items():
        value['pickrate'] = (100 * ((value['won'] + value['lost'])/total_picks))

    dict['totalpicks'] = total_picks


if __name__ == '__main__':
    main()