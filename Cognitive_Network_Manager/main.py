# Cognitive Network Manager
from flask import Flask, redirect, request, jsonify
import requests
import json

app = Flask(__name__)

# These URLs will be populated by the APM upon deployment
urls = {
    "Video_Client": ['http://localhost:5001', 'http://localhost:5002'],
    "Video_Server_Platform": 'http://localhost:5005',
    "UI": 'http://localhost:5000'
}

# This is the route the user first visits which sets up the connections
# and redirects the user to the video list
@app.route('/', methods=['GET', 'POST'])
def make_connections():
    # Redirect to the video list where the user chooses a video
    return redirect(str(urls['UI'])+'/', code=302)

# Route to send the chosen video from Video Server to Video Client
@app.route('/send_video', methods=['POST'])
def send_video():
    data = request.get_json()
    response = requests.post(str(urls['Video_Client'])+'/receive_video', json=data)

    return jsonify({"message": "Video sent to Video Client"})

if __name__ == '__main__':
    app.run(debug=True, port=5004)