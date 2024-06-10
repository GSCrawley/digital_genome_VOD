# Service Workflow Manager (SWM)
from flask import Flask, request, jsonify
import requests
import threading
import time

app = Flask(__name__)

video_clients = []
client_statuses = {}
lock = threading.Lock()

@app.route('/setup', methods=['POST'])
def setup():
    global video_clients, video_server
    data = request.get_json()
    video_clients = data['video_client']
    video_server = data['video_server']
    return "HI"

@app.route('/recover', methods=['GET', 'POST'])
def recover():
    for url in video_clients:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # TODO
                # Here is the Event for when a switch happens
                # EVENT
                data = {
                    "video_client": video_clients,
                    "video_server": video_server
                }
                # This reruns the setup when a new connection is established
                response = requests.get(f"{url}/setup", json=data)
                return jsonify(url)
        except:
            pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

