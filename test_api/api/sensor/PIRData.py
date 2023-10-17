from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from model import PirData
from . import sensorAPI
from bson import json_util
import json
from datetime import datetime
import pymongo
from Constant import Constants


uri = Constants["MONGODB_URL"]
client = MongoClient(uri, server_api=ServerApi('1'))
db = client[Constants["MONGODB_DB"]] 
collection = db[Constants["MONGODB_COLLECTION_PIR"]]

@sensorAPI.route('/', methods=['GET'])
def api_entry():
    response = {
        'data': "API is working"
    }
    return jsonify(response)

@sensorAPI.route('/get-pir', methods=['GET'])
def get_pir_by_id():
    sensor_id = request.args.get('sensor_id')
    pir_data = collection.find({'sensor_id': sensor_id}).sort('timestamp', pymongo.DESCENDING).limit(1)

    if pir_data:
        pir_data_json = json_util.dumps(pir_data[0])
        return pir_data_json, 200, {'Content-Type': 'application/json'}
    else:
        return jsonify({'message': 'Sensor not found'}), 404


@sensorAPI.route('/pir', methods=['POST'])
def post_data_to_pir():
    try:
        data = request.json
        sensor_id = data.get('sensor_id')
        status = data.get('status')
        van_id = data.get('van_id')
        val = data.get('value')

        pir_data = PirData(sensor_id, status, van_id, val)
        collection.insert_one(pir_data.__dict__)
        
        message = '{} Update!'.format(sensor_id)
        return jsonify({'message': message}), 200
    except Exception as e:
        error_message = f'An error occurred: {str(e)}'
        return jsonify({'error': error_message}), 500
