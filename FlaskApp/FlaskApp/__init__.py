import sys
from flask import Flask, render_template, request, jsonify

sys.path.insert(0, '/var/www/RiotAPIChallenge2.0/FlaskApp')
from FlaskApp.scripts.data_analytics.data_query import champions
from FlaskApp.scripts.data_retrieval import static_data
from FlaskApp.scripts.data_retrieval.static_data import static_io
from FlaskApp.scripts.data_retrieval.static_data.get_champion_data import get_sorted_champions

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'Kishan144'

REGIONS = static_data.regions
TIERS = static_data.highest_achieved_season_tier[::-1]
CHAMPIONS_ID = get_sorted_champions('id')
CHAMPIONS_NAME = get_sorted_champions('name')
CHAMPIONS_LENGTH = len(CHAMPIONS_ID)


#@app.route('/')
#def homepage():
#    return render_template("home.html")


@app.route('/blackmarketbrawlers')
def blackmarketbrawlers():
    return render_template("blackmarketbrawlers.html", regions=REGIONS, tiers=TIERS,
                           champions_id=CHAMPIONS_ID, champions_name=CHAMPIONS_NAME, champions_length=CHAMPIONS_LENGTH)


@app.route('/blackmarketbrawlers/champions', methods=['GET'])
def get_results():
    regions = request.args.getlist('r')
    tiers = request.args.getlist('t')
    result = champions.run_query(regions=regions, tiers=tiers)
    return jsonify(result)


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run()
