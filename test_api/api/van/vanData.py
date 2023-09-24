from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from model import VanData
from . import vanDataAPI
from datetime import datetime
from bson import json_util

uri = "mongodb+srv://riwara:Gso0u8f4JMR36d5G@newcluster.fxldupt.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['testDB'] 
collection = db['vanData']

@vanDataAPI.route('/', methods=['GET'])
def findvanbyid():
    response = {
        'data': "Van API is working"
    }
    return jsonify(response)

# Get van by ID
@vanDataAPI.route('/get-van', methods=['GET'])
def get_van_by_id():
    van_id = request.args.get('van_id')
    van = collection.find_one({'van_id': van_id})
    if van:
        van_json = json_util.dumps(van)
        return van_json, 200, {'Content-Type': 'application/json'}
    else:
        return jsonify({'message': 'Van not found'}), 404


@vanDataAPI.route('/van', methods=['POST'])
def create_van():
    request_data = request.json
    van_id = request_data.get('van_id')
    driver_name = request_data.get('driver_name')
    existing_van = collection.find_one({'van_id': van_id})

    if existing_van:
        collection.update_one({'van_id': van_id}, {
            '$set': {
                'driver_name': driver_name,
                'timestamp': datetime.now()
            }
        })
        message = 'Updated van information successfully'
    else:
        van = VanData(
            van_id=van_id,
            status=request_data.get('status', ''),
            image_data=request_data.get('image_data', ''),
            driver_name=driver_name,
            passenger=request_data.get('passenger', ''),
            speed=request_data.get('speed', 80)
        )
        collection.insert_one(van.__dict__)
        message = 'Created van successfully'

    return jsonify({'message': message})
