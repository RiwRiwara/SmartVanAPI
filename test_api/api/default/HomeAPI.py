from . import defaultAPI
from flask import  jsonify


@defaultAPI.route('/', methods=['GET'])
def api_entry():
    response = {
        'data': "API Running"
    }
    return jsonify(response)