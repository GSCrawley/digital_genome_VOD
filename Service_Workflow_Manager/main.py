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
    global video_clients, video_server, events, ui
    data = request.get_json()
    video_clients = data['video_client']
    video_server = data['video_server']
    events = data['Events']
    ui = data['UI']
    return "HI"

@app.route('/recover', methods=['GET', 'POST'])
def recover():
    for url in video_clients:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = {
                    "video_client": video_clients,
                    "video_server": video_server,
                    "Events": events
                }
                event_data = {
                    "video_client": url,
                    "ui": ui
                }
                requests.post(f'{events}/client_connection_event', json=event_data)
                print("DATA", events)
                response = requests.get(f"{url}/setup", json=data)
                return jsonify(url)
        except:
            pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)