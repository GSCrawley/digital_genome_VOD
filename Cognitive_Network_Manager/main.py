# Cognitive Network Manager (CNM)
from flask import Flask, redirect, request, jsonify
import requests
import json

app = Flask(__name__)

# These URLs will be populated by the APM upon deployment
urls = {
    "video_client":{"video_client": ['http://localhost:5001', 'http://localhost:5002'], "Events":'http://localhost:5006', "video_server":'http://localhost:5005'},
    "UI":{"UI":'http://localhost:5000', "SWM": 'http://localhost:5003', "video_client": ['http://localhost:5001', 'http://localhost:5002'], "Events":'http://localhost:5006', "User_Genome": "http://localhost:5007"},
    "SWM":{"SWM":'http://localhost:5003', "UI":'http://localhost:5000', 'video_client':['http://localhost:5001', 'http://localhost:5002'], "video_server":'http://localhost:5005', "Events":'http://localhost:5006'},
    "Events":{"Events":'http://localhost:5006', "CNM":'http://localhost:5004', "UI":'http://localhost:5000', "SWM":'http://localhost:5003', "video_client": ['http://localhost:5001', 'http://localhost:5002'], "video_server":'http://localhost:5005'},
    "User_Genome":{"User_Genome": 'http://localhost:5007', "Events": 'http://localhost:5006'}
}

# This is the route the user first visits which sets up the connections
# and reroutes thr user to the UI. This makes the communication for each 
# node non-dependent on a hard coded URL.
# @app.route('/', methods=['GET', 'POST'])
def make_connections():
    data = urls["Events"]
    response = requests.post(str(data["Events"])+'/structural_setup_event', json=data)
    # Making SWM Connections to communicate
    data = urls["SWM"]
    response = requests.post(str(data["SWM"])+'/setup', json=data)

    # Making UI connections to communicate to SWM
    data = urls["UI"]
    print(data)
    response = requests.post(str(data['UI'])+'/setup', json=data)

    # Making User_Genome connections
    data = urls["User_Genome"]
    response = requests.post(str(data['User_Genome'])+'/setup', json=data)

    # Makeing video_client connections
    data = urls["video_client"]
    for url in data["video_client"]:
        try:
            response = requests.post(url+'/setup', json=data)
        except:
            pass

    # setup event

    # When finished redirect to the UI
    # return redirect(str(urls['UI']['UI']), code=302)
    return('Hi')

make_connections()


if __name__ == '__main__':
    app.run(debug=True, port=5004)