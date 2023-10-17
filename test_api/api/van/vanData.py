from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from model import VanData
from . import vanDataAPI
from datetime import datetime
from bson import json_util
from Constant import Constants


uri = Constants["MONGODB_URL"]
client = MongoClient(uri, server_api=ServerApi('1'))
db = client[Constants["MONGODB_DB"]] 
collection = db[Constants["MONGODB_COLLECTION_VAN"]]

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
# get all van
@vanDataAPI.route('/get-all-van', methods=['GET'])
def get_all_van():
    vans = collection.find()
    if vans:
        vans_json = json_util.dumps(vans)
        return vans_json, 200, {'Content-Type': 'application/json'}
    else:
        return jsonify({'message': 'Van not found'}), 404


@vanDataAPI.route('/van', methods=['POST'])
def create_van():
    request_data = request.json
    van_id = request_data.get('van_id')
    driver_name = request_data.get('driver_name')
    isOpenNotification = request_data.get('isOpenNotification')
    existing_van = collection.find_one({'van_id': van_id})

    if existing_van:
        updated_van_data = {}
        # Check if each field exists in the request data and has changed
        if 'status' in request_data and request_data['status'] != existing_van['status']:
            updated_van_data['status'] = request_data['status']

        if 'image_data' in request_data and request_data['image_data'] != existing_van['image_data']:
            updated_van_data['image_data'] = request_data['image_data']

        if driver_name != existing_van['driver_name']:
            updated_van_data['driver_name'] = driver_name

        if 'passenger' in request_data and request_data['passenger'] != existing_van['passenger']:
            updated_van_data['passenger'] = request_data['passenger']

        if 'speed' in request_data and request_data['speed'] != existing_van['speed']:
            updated_van_data['speed'] = request_data['speed']

        if isOpenNotification != existing_van['isOpenNotification']:
            updated_van_data['isOpenNotification'] = isOpenNotification

        if updated_van_data:
            updated_van_data['updated_at'] = datetime.now()
            collection.update_one({'van_id': van_id}, {'$set': updated_van_data})
            message = 'Updated van information successfully'
        else:
            message = 'No changes to update'
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

@vanDataAPI.route('/van/<van_id>', methods=['DELETE'])
def delete_van(van_id):
    van = collection.find_one({'van_id': van_id})

    if van:
        collection.delete_one({'van_id': van_id})
        message = f'Deleted van with ID: {van_id}'
        status_code = 200
    else:
        message = f'Van with ID {van_id} not found'
        status_code = 404

    return jsonify({'message': message}), status_code