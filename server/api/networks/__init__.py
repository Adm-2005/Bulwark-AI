from flask import Blueprint

net_bp = Blueprint('networks', __name__)

from . import routes