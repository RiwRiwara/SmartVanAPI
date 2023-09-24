from flask import Blueprint

sensorAPI = Blueprint('sensorAPI', __name__)

from . import PIRData, Notify, CAMData
