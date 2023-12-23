from flask import Blueprint
from .models import Post

post_bp = Blueprint('post_bp', __name__, template_folder='templates/post')

from . import views
