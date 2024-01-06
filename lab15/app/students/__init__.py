from flask import Blueprint

students_bp = Blueprint("students_bp", __name__, url_prefix='/students_bp')

from . import models