from flask import Blueprint
from flask_login import LoginManager

users = Blueprint('users', __name__, template_folder='templates/users')

from . import views