# Events
from flask import Flask, request, jsonify
from tigerGraph import video_selected_event, user_registration_event, validate_login
from structuralGraph import structural_setup_event, client_connection_event, create_video_client_event

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Events Server Working'

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user_registration_event(data)
    return jsonify({"message": "User registered successfully"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    result = validate_login(email, password)
    if result == 'Fail':
        return jsonify({"message": "Fail"}), 500
    else:
        return jsonify(result), 200

@app.route('/video_selected_event', methods=['GET', 'POST'])
def video_selected():
    data = request.get_json()
    # send data to tigergraph
    print("Video SELECTED")
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