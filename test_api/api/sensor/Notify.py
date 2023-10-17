from flask import Blueprint, request, jsonify
import requests
from . import sensorAPI
from Constant import Constants


LINE_NOTIFY_TOKEN = Constants["LINE_NOTIFY_TOKEN"]
LINE_NOTIFY_API_URL = Constants["LINE_NOTIFY_API_URL"]

@sensorAPI.route('/send_notification', methods=['POST'])
def send_notification():
    message = request.form.get('message')
    is_enable = request.form.get('isEnable') # 0: disable, 1: enable
    
    if is_enable == "0":
        return jsonify({"message": "Notification sending is not enabled"}), 400

    headers = {
        'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}',
    }

    payload = {'message': message}

    try:
        response = requests.post(LINE_NOTIFY_API_URL, headers=headers, data=payload)

        if response.status_code == 200:
            return jsonify({"message": "Notification sent successfully"}), 200
        else:
            return jsonify({"message": f"Failed to send notification: {response.text}"}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"message": f"Failed to send notification: {str(e)}"}), 500