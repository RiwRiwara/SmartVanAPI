from flask import Blueprint

vanDataAPI = Blueprint('vanDataAPI', __name__)

from . import vanData
