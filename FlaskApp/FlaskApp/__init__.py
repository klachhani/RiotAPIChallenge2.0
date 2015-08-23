from flask import Flask, render_template, request, jsonify

from FlaskApp.scritps.data_analytics.data_query import champions

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


@app.route('/blackmarketbrawlers/query', methods=['GET', 'POST'])
def get_results():
    regions = []
    tiers = []

    #if request.method == 'POST':
    #    regions = request.json['regions']
    #    tiers = request.json['tiers']

    #if request.method == 'GET':
    #    result = champions.run_query(regions=regions, tiers=tiers)
    #    result = jsonify(result)
    #    return result

    return 'none'



@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run()
