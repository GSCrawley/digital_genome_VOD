# Cognitive Network Manager
from flask import Flask, redirect, request, jsonify
import requests
import json

app = Flask(__name__)

# These URLs will be populated by the APM upon deployment
urls = {
    # "client_server": ['http://localhost:5001', 'http://localhost:5002'],
    "video_client":{"video_client": ['http://localhost:5001', 'http://localhost:5002'], "video_server":'http://localhost:5005'},
    # "SWM": 'http://localhost:5003',
    "UI":{"UI":'http://localhost:5000', "SWM": 'http://localhost:5003', "video_client": ['http://localhost:5001', 'http://localhost:5002']},
    # 'SWM': {'video_client':5001, 'video_server': 5002}
    # 'video_server: 5002'
}

# This is the route the user first visits which sets up the connections
# and reroutes thr user to the UI. This makes the communication for each 
# node non-dependent on a hard coded URL.
@app.route('/', methods=['GET', 'POST'])
def make_connections():
    # Making UI connections to communicate to SWM
    data = urls["UI"]
    response = requests.post(str(urls['UI']['UI'])+'/setup', json=data)

    # Makeing video_client connections
    data = urls["video_client"]
    for url in urls["video_client"]["video_client"]:
        try:
            response = requests.post(url+'/setup', json=data)
        except:
            pass

    # Making SWM Connections to communicate to client server
    # data = {
    #     "Client": urls['client_server']
    # }
    # response = requests.post(str(urls['SWM'])+'/setup', json=data)

    # When finished redirect to the UI
    return redirect(str(urls['UI']['UI']), code=302)


if __name__ == '__main__':
    app.run(debug=True, port=5004)