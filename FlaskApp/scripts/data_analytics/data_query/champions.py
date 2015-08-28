from __future__ import division

__author__ = 'Kishan'

from FlaskApp.scripts.data_analytics.data_query import query_io as query_io
from FlaskApp.scripts.data_retrieval.static_data import static_io as static_io
from FlaskApp.scripts.data_retrieval import static_data
from FlaskApp.scripts.data_analytics.data_filter import champions as champ
from collections import OrderedDict

def run_query(regions, tiers):
    if len(regions) == 0:
        regions = static_data.regions
    if len(tiers) == 0:
        tiers = static_data.highest_achieved_season_tier
    outcome = ['won', 'lost', 'total']

    champions = static_io.read_json('champions_by_id.json')

    data = query_io.read_json('champions.json')

    result = {}

    create_empty_result_dict(result, champions, outcome)
    query_champions_json(result, data, regions, tiers, outcome, champions)
    calculate_extras(result)


    final_result = {}
    for o in outcome:
        final_result[o] = []
        for c in result:
            dict = OrderedDict({'id' : c, 'name' : champions[c]['name'], 'key' : champions[c]['key']})
            dict.update(sorted((result[c][o]).items()))
            final_result[o].append(dict)

    return final_result


def query_champions_json(result, data, regions, tiers, outcome, champions):
    region = (r for r in data.keys() if r in regions)
    for r in region:
        tier = (t for t in data[r].keys() if t in tiers)
        for t in tier:
            champion = (c for c in data[r][t].keys() if c in champions)
            for c in champion:
                for o in outcome:
                    result[c][o]['picks'] += (data[r][t][c][o]['picks']
                                              if not o == 'total'
                                              else data[r][t][c]['won']['picks']
                                                   + data[r][t][c]['lost']['picks'])
                    result[c][o]['matchDuration'] += (data[r][t][c][o]['matchDuration']
                                                      if not o == 'total'
                                                      else data[r][t][c]['won']['matchDuration']
                                                           + data[r][t][c]['lost']['matchDuration'])
                    for s in champ.stat_titles:
                        result[c][o][s] += (data[r][t][c][o][s]
                                            if not o == 'total'
                                            else data[r][t][c]['won'][s]
                                                 + data[r][t][c]['lost'][s])
                for o in outcome:
                    for s in champ.stat_titles:
                        result[c][o][s + '-per5min'] = float("%.3f" % ((
                            (result[c][o][s] / result[c][o]['matchDuration'] * 300
                             if not result[c][o]['matchDuration'] == 0 else 0)
                            if not o == 'total' else (
                            (result[c]['won'][s + '-per5min'] + result[c]['lost'][s]) / (
                                result[c]['won']['matchDuration'] + result[c]['lost'][
                                    'matchDuration']) * 300 if not (result[c]['won'][
                                                                        'matchDuration'] +
                                                                    result[c]['lost'][
                                                                        'matchDuration']) == 0
                            else 0))))


def create_empty_result_dict(result, champions, outcome):
    for c in champions.keys():
        result[c] = {}
        for o in outcome:
            result[c][o] = {}
            result[c][o]['picks'] = 0
            result[c][o]['matchDuration'] = 0
            for s in champ.stat_titles:
                result[c][o][s] = 0
                result[c][o][s + '-per5min'] = 0


def calculate_extras(result):
    total_picks = {'won' : 0, 'lost' : 0, 'total' : 0}
    for c in result:
        for o in result[c]:
            total_picks[o] += result[c][o]['picks']
        champ_picks = result[c]['won']['picks'] + result[c]['lost']['picks']
        result[c]['total']['winrate'] = result[c]['won']['winrate'] = result[c]['lost'][
            'winrate'] = float("%.3f" % ((100 * result[c]['won']['picks'] / champ_picks) if not champ_picks == 0 else 0))

    for c in result:
        for o in result[c]:
            result[c][o]['pickrate'] = float("%.3f" % ((100*result[c][o]['picks']/total_picks[o]) if not total_picks == 0 else 0))


if __name__ == '__main__':
    run_query([], [])
