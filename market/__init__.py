from re import template
from flask import Flask
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#add a configuration so Flask is able to handle database, grab the app and apply the method, this tell Flask where th DB is
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '5314491eabf4bcff839dd26e'
db = SQLAlchemy(app)

from market import routes