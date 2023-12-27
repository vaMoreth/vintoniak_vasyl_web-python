from flask import Blueprint
from flask_login import LoginManager

auth = Blueprint('auth', __name__, template_folder='templates/auth')

from . import views
