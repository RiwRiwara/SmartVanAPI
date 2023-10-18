from flask import Blueprint, request, jsonify
import requests
from . import sensorAPI
from Constant import Constants
import datetime
import json


LINE_NOTIFY_TOKEN = Constants["LINE_NOTIFY_TOKEN"]
LINE_NOTIFY_API_URL = Constants["LINE_NOTIFY_API_URL"]

@sensorAPI.route('/send_notification', methods=['POST'])
def send_notification():
    message = request.form.get('message')
    vanID = request.form.get('vanID')

    van_api_url = f'http://{Constants["HOST"]}:{Constants["PORT"]}/api/van/get-van?van_id={vanID}'
    vandata = requests.get(van_api_url).json()
    vanOBJ = vandata

    DateNowStr = datetime.datetime.now().strftime("%d/%m/%Y")
    TimeNowStr = datetime.datetime.now().strftime("%H:%M:%S")
    if vanOBJ['isOpenNotification'] == "0":
        return jsonify({"message": "Notification sending is not enabled"}), 400

    headers = {
        'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}',
    }

    

    payload = {'message': "\nวันที่ : "+DateNowStr+"\n"+
                          "เวลา : "+TimeNowStr+"\n"+
                          "ข้อความ : "+  message + "\n"+
                          f"""----- [ข้อมูลรถ] -----
ชื่อคนขับ {vanOBJ['driver_name']}
ทะเบียนรถ {vanOBJ['van_id']}
Video 1 : {Constants['CAM1_URL']}
Video 2 : {Constants['CAM2_URL']}
----- ดูข้อมูลเพิ่มเติม ----- 
http://{Constants['HOST']}:{Constants['PORT_FRONTEND']}/van/{vanOBJ['van_id']}
"""
                          }

    try:
        response = requests.post(LINE_NOTIFY_API_URL, headers=headers, data=payload)

        if response.status_code == 200:
            return jsonify({"message": "Notification sent successfully"}), 200
        else:
            return jsonify({"message": f"Failed to send notification: {response.text}"}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"message": f"Failed to send notification: {str(e)}"}), 500