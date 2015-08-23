from flask import Flask, render_template, request, flash, jsonify
from FlaskApp.FlaskApp.scritps.data_analytics.data_query import champions

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'Kishan144'


@app.route('/')
def homepage():
    return render_template("home.html")


@app.route('/blackmarketbrawlers')
def blackmarketbrawlers():
    regions = ['br', 'eune', 'euw', 'kr', 'lan', 'las', 'na', 'oce', 'ru', 'tr']
    tiers = ['UNRANKED', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER', 'CHALLENGER']
    return render_template("blackmarketbrawlers.html", regions=regions, tiers=tiers)


@app.route('/blackmarketbrawlers/query', methods=['POST'])
def get_results():
    json = request.json
    print(json)
    print(champions.run_query(regions=json['regions'], tiers=json['tiers']))
    return jsonify(json)

@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run()
