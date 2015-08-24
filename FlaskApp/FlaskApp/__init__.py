import sys
from flask import Flask, render_template, request, jsonify

#sys.path.append('/var/www/RiotAPIChallenge2.0')
from FlaskApp.scritps.data_analytics.data_query import champions
from FlaskApp.scritps.data_analytics.data_query import *



app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'Kishan144'

REGIONS = ['br', 'eune', 'euw', 'kr', 'lan', 'las', 'na', 'oce', 'ru', 'tr']
TIERS = ['UNRANKED', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER', 'CHALLENGER']

@app.route('/')
def homepage():
    return render_template("home.html")


@app.route('/blackmarketbrawlers')
def blackmarketbrawlers():

    return render_template("blackmarketbrawlers.html", regions=REGIONS, tiers=TIERS)


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
