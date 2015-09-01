__author__ = 'Kishan'

from FlaskApp.scripts.data_retrieval.match_data import get_match_data
from FlaskApp.scripts.data_retrieval import static_data
from FlaskApp.scripts.data_retrieval.static_data import static_io as static_io
from FlaskApp.scripts.data_analytics.data_query import query_io as query_io


# Run query to aggregate releveant data
def run_query(regions = get_match_data.get_match_regions(), tiers = static_data.highest_achieved_season_tier):

    minions = static_io.read_json('minions_by_id.json')
    upgrades = static_io.read_json('upgrades_by_id.json')

    data = query_io.read_json('minions.json')

    result = {}

    create_query_result_dict(result, minions, upgrades)
    query_minions_json(result, data, regions, tiers, minions, upgrades)
    calculate_extras(result)

    query_io.write_json(result, 'test.json')

    return result_breakdown(result)

# Cumulate relevant data according the query and evaluate other releveant information from this
def query_minions_json(result, data, regions, tiers, minions, upgrades):
    region = (r for r in data.keys() if r in regions)
    for r in region:
        tier = (t for t in data[r].keys() if t in tiers)
        for t in tier:
            minion = (m for m in data[r][t].keys() if m in minions)
            for m in minion:
                result[m]['won'] += data[r][t][m]['won']
                result[m]['lost'] += data[r][t][m]['lost']
                upgrade = (u for u in data[r][t][m].keys() if u in upgrades)
                for u in upgrade:
                    result[m][u]['won'] += data[r][t][m][u]['won']
                    result[m][u]['lost'] += data[r][t][m][u]['lost']


# Create empty dict which will be populated with accumulated/aggregated data
# dict[minion][upgrade]
def create_query_result_dict(result, minions, upgrades):
    for minion_id, minion_name in minions.items():
        result[minion_id] = {'name' : minion_name, 'won' : 0, 'lost' : 0}
        for upgrade_id, upgrade_name in upgrades.items():
            result[minion_id][upgrade_id] = {'name' : upgrade_name, 'won' : 0,  'lost' : 0}

# Evaluate any other stats which can be done after other data has been aggregated
def calculate_extras(result):
    total_minion_picks = 0
    for m, minion in result.items():
        total_minion_picks += minion['won'] + minion['lost']
        minion_picks = minion['won'] + minion['lost']
        minion['winrate'] = float("%.3f" % (100 * (minion['won'] / minion_picks)) if not minion_picks == 0 else '0')

    for m, minion in result.items():
        minion_picks = float(minion['won'] + minion['lost'])
        minion['pickrate'] = float("%.3f" % (100 * (minion_picks / total_minion_picks)) if not total_minion_picks == 0 else '0')
        for u, upgrade in minion.items():
            if not type(upgrade) == type({}): continue
            upgrade_picks = float(upgrade['won'] + upgrade['lost'])
            upgrade['pickrate'] = float("%.3f" % ((100 * (upgrade_picks / minion_picks)) if not minion_picks == 0 else 0))
            upgrade['winrate'] = float("%.3f" % ((100 * (upgrade['won'] / upgrade_picks)) if not upgrade_picks == 0 else 0))


# Reformat and sort data to prepare for d3.js
def result_breakdown(result):
    winrate = []
    pickrate = []
    upgrade_pickrate = {}

    for m, minion in result.items():
        winrate.append([m, minion['name'], minion['winrate']])
        pickrate.append([m, minion['name'], minion['pickrate'], minion['won'] + minion['lost']])
        for u, upgrade in minion.items():
            if not type(upgrade) == type({}): continue
            if not minion['name'] in upgrade_pickrate: upgrade_pickrate[minion['name']] = []
            upgrade_pickrate[minion['name']].append([u, upgrade['name'], upgrade['pickrate']])

    winrate = sorted(sorted(winrate, key=lambda x: x[1], reverse=False), key=lambda x: x[2], reverse=True)
    pickrate = sorted(sorted(pickrate, key=lambda x: x[1], reverse=False), key=lambda x: x[2], reverse=True)

    for minion, upgrades in upgrade_pickrate.items():
        upgrade_pickrate[minion] = sorted(sorted(upgrades, key=lambda x: x[2], reverse=True), key=lambda x: x[1], reverse=False)

    return {'winrate': winrate,
            'pickrate': pickrate,
            'upgrade_pickrate' : upgrade_pickrate}


if __name__ == '__main__':
    run_query()
