from flask import Flask
from flask_cors import CORS
from api.sensor import sensorAPI
from api.van import vanDataAPI

app = Flask(__name__)
CORS(app)

app.register_blueprint(sensorAPI, url_prefix='/api/sensor')
app.register_blueprint(vanDataAPI, url_prefix='/api/van')

if __name__ == '__main__':
    app.run(host='192.168.1.10', port=5565, debug=True)
