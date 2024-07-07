# Events
from flask import Flask, request
from tigerGraph import video_selected_event
from structuralGraph import structural_setup_event, client_connection_event, create_video_client_event

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Events Server Working'

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    # Here you would typically validate the data and create a new user in TigerGraph
    # For now, let's just print the data and return a success message
    print("Registering new user:", data)
    # TODO: Implement user creation in TigerGraph
    return jsonify({"message": "User registered successfully"}), 200

@app.route('/video_selected_event', methods=['GET', 'POST'])
def video_selected():
    data = request.get_json()
    # send data to tigergraph
    video_selected_event(data)
    return("HI")

@app.route('/structural_setup_event', methods=['GET', 'POST'])
def setup_event():
    data = request.get_json()
    structural_setup_event(data)
    return("HI")

@app.route('/client_connection_event', methods=['GET', 'POST'])
def connection_event():
    data = request.get_json()
    client_connection_event(data)
    return("HI")

@app.route('/create_video_client_event', methods=['GET', 'POST'])
def create_video_client():
    data = request.get_json()
    create_video_client_event(data)
    return("HI")


if __name__ == '__main__':
    app.run(debug=True, port=5006)
