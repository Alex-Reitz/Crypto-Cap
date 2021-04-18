import os

from flask import Flask, url_for, render_template, redirect, flash, jsonify, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import UserAddForm, LoginForm
from models import db, connect_db, User, Favorites, Cryptos
from dotenv import load_dotenv

from api import Crypto
crypto = Crypto()

app = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "abcdef"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///capCoin"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CURR_USER_KEY = "curr_user"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

#_____BEFORE EACH REQUEST_____#
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

#_____Authentication/Authorization Routes_____#
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

#_____HOME PAGE____#
@app.route("/")
def home_page():
    """Show Homepage with top 25 cryptos by market cap"""
    output = crypto.get_top_25()
    for result in output:
        result['quote']['USD']['price'] = '$ ' + "{:,.2f}".format(result['quote']['USD']['price'])
        result['quote']['USD']['market_cap'] = '$ ' + "{:,.2f}".format(result['quote']['USD']['market_cap'])
    return render_template('home.html', **locals())
