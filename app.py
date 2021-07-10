import os
import requests
import json
from requests import Request, Session
from requests.auth import HTTPBasicAuth
from flask import Flask, url_for, render_template, redirect, flash, jsonify, session, g, request
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import UserAddForm, LoginForm
from models import db, connect_db, User

from api import Crypto
crypto = Crypto()
api_key = os.environ.get("API_KEY")

app = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "secret_key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///capCoin"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CURR_USER_KEY = "curr_user"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

#Before each request
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global"""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None
def do_login(user):
    """Log in user"""
    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

#Authentication/Authorization Routes
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """New User Signup Functionality"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)
        do_login(user)
        return redirect("/")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Login Functionality"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Logout Function"""
    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")

#Home page
@app.route("/")
def home_page():
    """Show Homepage with top 25 cryptos by market cap"""
    if g.user:
        user_faves = g.user.favorites
    else:
        user_faves = [];
    output = crypto.get_top_200()
    
    for result in output:
        result['quote']['USD']['price'] = '$' + "{:,.2f}".format(result['quote']['USD']['price'])
        result['quote']['USD']['market_cap'] = '$' + "{:,.2f}".format(result['quote']['USD']['market_cap'])
        result['total_supply'] = "{:,.0f}".format(result['total_supply'])
    for result in output:
        if result['slug'] in user_faves:
            result["favorite"] = True
    
    """ Output looks like this {'id': 1, 'name': 'Bitcoin', 'symbol': 'BTC', 'slug': 'bitcoin', 'num_market_pairs': 9030, 'date_added': '2013-04-28T00:00:00.000Z', 
    'tags': ['mineable', 'pow', 'sha-256', 'store-of-value', 'state-channels', 'coinbase-ventures-portfolio', 'three-arrows-capital-portfolio', 'polychain-capital-portfolio', 'binance-labs-portfolio', 'arrington-xrp-capital', 'blockchain-capital-portfolio', 'boostvc-portfolio', 'cms-holdings-portfolio', 'dcg-portfolio', 'dragonfly-capital-portfolio', 'electric-capital-portfolio', 'fabric-ventures-portfolio', 'framework-ventures', 'galaxy-digital-portfolio', 'huobi-capital', 'alameda-research-portfolio', 'a16z-portfolio', '1confirmation-portfolio', 'winklevoss-capital', 'usv-portfolio', 'placeholder-ventures-portfolio', 'pantera-capital-portfolio', 'multicoin-capital-portfolio', 'paradigm-xzy-screener'], 
    'max_supply': 21000000, 'circulating_supply': 18752037, 'total_supply': 18752037, 'platform': None, 'cmc_rank': 1, 'last_updated': '2021-07-09T21:58:02.000Z', 
    'quote': {'USD': {'price': '$33,879.96', 'volume_24h': 27204317563.446537, 'percent_change_1h': 1.07943697, 'percent_change_24h': 3.53574286, 'percent_change_7d': 1.09199452, 'percent_change_30d': -7.66137093, 'percent_change_60d': -39.27195248, 'percent_change_90d': -42.63507675, 'market_cap': '$635,318,247,111.33', 'last_updated': '2021-07-09T21:58:02.000Z'}}, 'favorite': True} """
    return render_template('home.html', output=output, user_faves=user_faves)

#Syntax: url_for('name of the function of the route','parameters (if required)')
#Route for specific crypto in top 25
@app.route('/crypto/<string:name>/<int:id>', methods=['GET'])
def get_crypto_id(name,id):
    return render_template('crypto.html', name=name, id=id)

@app.route("/api/load_info", methods=["POST"])
def load_info():
    cmc_id = request.json["id"]
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
    headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': api_key,
        }
    parameters = {
          'id': cmc_id
    }
    session = Session()
    session.headers.update(headers)
    response = session.get(url, headers=headers, params=parameters)
    data = json.loads(response.text)
    crypto_id = data['data'][cmc_id]["id"]
    return data['data'][cmc_id]

#Route for when a User clicks on their name in nav bar
@app.route('/users/<int:user_id>', methods=["GET", "POST"])
def show_user_profile(user_id):
    """Show a User's profile"""
    if not g.user:
        flash("Please login", "danger")
        redirect("/")
    user = User.query.get_or_404(user_id)
    user_faves = g.user.favorites
    
    return render_template('show_profile.html', user=user, favorites=user_faves)

#----------
#Favorites
#----------

#API endpoint for toggling a favorite, selected = fa-star fas non-selected = far fa-star
@app.route("/api/toggle_favorite", methods=["GET", "POST"])
def toggle_favorite():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    cmc_id = request.json["id"]
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
    headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': api_key,
        }
    parameters = {
          'id': cmc_id
        }
    session = Session()
    session.headers.update(headers)
    response = session.get(url, headers=headers, params=parameters)
    data = json.loads(response.text)
    favorited_crypto = data['data'][cmc_id]['slug']
    user_id = g.user.id
    user_info = User.query.get(user_id)
    user_faves = g.user.favorites
    if favorited_crypto in user_faves:
        g.user.favorites = [favorite for favorite in user_faves if favorite != favorited_crypto]
    else:
        user_info.favorites.append(favorited_crypto)
    db.session.commit()
    return "toggled"
    

#Show user favorites
@app.route("/users/<int:user_id>/favorites", methods=["GET", "POST"])
def show_favorites(user_id):
    if not g.user:
        flash("Please login", "danger")
        redirect("/")
    user = User.query.get_or_404(user_id)
    user_faves = g.user.favorites
    fav_string = ",".join(str(x) for x in user_faves)
    
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
    headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': api_key,
        }
    parameters = {
        'slug': fav_string
        }
    session = Session()
    session.headers.update(headers)
    response = session.get(url, headers=headers, params=parameters)
    data = json.loads(response.text)
    if len(g.user.favorites) == 0:
        newData = [];
    else:    
        newData = data['data'].values()
    for result in newData:
        if result['slug'] in user_faves:
            result["favorite"] = True
    return render_template('favorites.html', newData=newData)


