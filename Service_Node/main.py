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
    global video_clients, client_statuses
    data = request.get_json()
    video_clients = data['video_client']
    client_statuses = {client: True for client in video_clients}
    # for client in video_clients:
    #     threading.Thread(target=check_client_status, args=(client,), daemon=True).start()
    return "HI"

def check_client_status(client_url):
    while True:
        try:
            response = requests.get(client_url + '/health_check')
            with lock:
                client_statuses[client_url] = (response.status_code == 200)
        except requests.exceptions.RequestException:
            with lock:
                client_statuses[client_url] = False
        time.sleep(5)

@app.route('/current_client', methods=['GET'])
def current_client():
    client_list = []
    with lock:
        for client, status in client_statuses.items():
            if status:
                client_list.append(client)
        return jsonify({'client_url': client_list})
    return jsonify({'error': 'No available video clients'}), 500

@app.route('/health_check', methods=['GET'])
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)