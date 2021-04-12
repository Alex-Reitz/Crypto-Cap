from flask import Flask, url_for, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db

app = Flask(__name__)
app.config['SECRET_KEY'] = "abcdef"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route("/")
def home_page():
    return render_template("home.html")