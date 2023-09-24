from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from model import CameraData
from . import sensorAPI
from bson import json_util
import json
from datetime import datetime

uri = "mongodb+srv://riwara:Gso0u8f4JMR36d5G@newcluster.fxldupt.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['testDB'] 
collection = db['camdata']

@sensorAPI.route('/', methods=['GET'])
def api_entry_cam():
    response = {
        'data': "CAM API is working"
    }
    return jsonify(response)

# Get cam by ID
@sensorAPI.route('/get-camera', methods=['GET'])
def get_cam_by_id():
    sensor_id = request.args.get('sensor_id')
    van = collection.find_one({'sensor_id': sensor_id})
    if van:
        van_json = json_util.dumps(van)
        return van_json, 200, {'Content-Type': 'application/json'}
    else:
        return jsonify({'message': 'camera not found'}), 404


@sensorAPI.route('/camera', methods=['POST'])
def post_data_to_cam():
    try:
        data = request.json
        sensor_id = data.get('sensor_id')
        status = data.get('status')
        image_data = data.get('image_data', '')  

        cam_data = CameraData(sensor_id, status, image_data)
        collection.insert_one(cam_data.__dict__)
        message = 'CAM data successfully created'
        return jsonify({'message': message}), 200

    except Exception as e:
        error_message = f'An error occurred: {str(e)}'
        return jsonify({'error': error_message}), 500
