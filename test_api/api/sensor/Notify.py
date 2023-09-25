from flask import Blueprint, request, jsonify
import requests
from . import sensorAPI
from Constant import Constants


LINE_NOTIFY_TOKEN = Constants["LINE_NOTIFY_TOKEN"]
LINE_NOTIFY_API_URL = Constants["LINE_NOTIFY_API_URL"]

@sensorAPI.route('/send_notification', methods=['POST'])
def send_notification():
    message = request.form.get('message')

    headers = {
        'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}',
    }
    if request.content_type == 'application/x-www-form-urlencoded':
        payload = {'message': message}
        response = requests.post(LINE_NOTIFY_API_URL, headers=headers, data=payload)
    elif request.content_type == 'multipart/form-data':
        payload = [('message', message)]
        response = requests.post(LINE_NOTIFY_API_URL, headers=headers, data=payload)

    if response.status_code == 200:
        return jsonify({"message": "Notification sent successfully"})
    else:
        return jsonify({"message": f"Failed to send notification: {response.text}"}), response.status_code
