# Cognitive Network Manager
from flask import Flask, redirect, request, jsonify
import requests
import json

app = Flask(__name__)

# These URLs will be populated by the APM upon deployment
urls = {
    "client_server": ['http://localhost:5001', 'http://localhost:5002'],
    "SWM": 'http://localhost:5003',
    "UI": 'http://localhost:5000'
}

# This is the route the user first visits which sets up the connections
# and reroutes thr user to the UI. This makes the communication for each 
# node non-dependent on a hard coded URL.
@app.route('/', methods=['GET', 'POST'])
def make_connections():
    # Making UI connections to communicate to SWM
    data = {
        "SWM": urls['SWM']
    }
    response = requests.post(str(urls['UI'])+'/setup', json=data)

    # Making SWM Connections to communicate to client server
    data = {
        "Client": urls['client_server']
    }
    response = requests.post(str(urls['SWM'])+'/setup', json=data)

    # When finished redirect to the UI
    return redirect(str(urls['UI']), code=302)


if __name__ == '__main__':
    app.run(debug=True, port=5004)