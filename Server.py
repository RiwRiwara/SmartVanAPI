from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    response = {
        'data': {
            'value': 'Hello World!'
        }
    }
    return jsonify(response)

@app.route('/api/pir', methods=['POST'])
def post_data_to_sensor1():
    data = request.json  
    print("Received data from /api/sensor1:", data)
    return jsonify({'message': 'Data received successfully for sensor1'})

if __name__ == '__main__':
    app.run(host='192.168.1.10', port=5565, debug=True)

