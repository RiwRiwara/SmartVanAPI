from . import defaultAPI
from flask import Blueprint, request, jsonify
from model import SystemConfiguration
from Constant import Constants
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from bson import json_util
from bson import ObjectId


uri = Constants["MONGODB_URL"]
client = MongoClient(uri, server_api=ServerApi('1'))
db = client[Constants["MONGODB_DB"]] 
collection = db[Constants["MONGODB_COLLECTION_WEB"]]

@defaultAPI.route('/', methods=['GET'])
def api_entry():
    response = {
        'data': "API Running"
    }
    return jsonify(response)

@defaultAPI.route('/setting', methods=['GET'])
def getSetting():
    id = request.args.get('id')
    setting = collection.find_one({'id': id})
    try:
        if setting:
            setting['_id'] = str(setting['_id'])
            return jsonify(setting)
        else:
            return jsonify({'message': 'Setting not found'}), 404

    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred'}), 500
    
@defaultAPI.route('/setting', methods=['POST'])
def setting():
    request_data = request.json
    id = request_data.get('id')
    status = request_data.get('status')
    isOpenNotification = request_data.get('isOpenNotification')
    startTime = request_data.get('startTime')
    endTime = request_data.get('endTime')
    listDay = request_data.get('listDay')
    
    existing_setting = collection.find_one({'id': id})
    if existing_setting:
        update_fields = {}

        if isOpenNotification is not None:
            update_fields['isOpenNotification'] = isOpenNotification

        if startTime is not None:
            update_fields['startTime'] = startTime

        if endTime is not None:
            update_fields['endTime'] = endTime

        if listDay is not None:
            update_fields['listDay'] = listDay
        collection.update_one({'id': id}, {'$set': update_fields})

        return jsonify({'message': 'Setting updated successfully'})
    else:
        # Create a new setting
        new_setting = {
            'id': id, # 'id': '1
            'status': status,
            'isOpenNotification': isOpenNotification,
            'startTime': startTime,
            'endTime': endTime,
            'listDay': listDay
        }
        collection.insert_one(new_setting)
        return jsonify({'message': 'New setting created successfully'})