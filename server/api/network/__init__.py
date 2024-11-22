from flask import Blueprint

net_bp = Blueprint('network', __name__)

from . import routes