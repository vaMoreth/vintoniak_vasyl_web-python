from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = b"secret"
app.permanent_session_lifetime = timedelta(days=30)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'site.sqlite')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views