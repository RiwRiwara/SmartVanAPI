from . import defaultAPI
from flask import  jsonify


@defaultAPI.route('/', methods=['GET'])
def api_entry():
    response = {
        'data': "API Running"
    }
    return jsonify(response)

# @defaultAPI.route('/get-cam', methods=['GET'])
# def api_getvideo():

#     return 0