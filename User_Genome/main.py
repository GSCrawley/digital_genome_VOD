import config
# import openai
from flask import Flask, jsonify, request, session, g
from flask_jwt_extended import JWTManager, jwt_required, \
                               create_access_token
import requests, names, random, threading, uuid, json
import argparse

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import requests
import config

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
jwt = JWTManager(app)

event_url = "http://localhost:5000"  # Assuming the Events node is running on localhost:5000

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response = requests.post(f"{event_url}/register", json=data)
    if response.status_code == 200:
        user_data = response.json()
        return jsonify({"message": "Registration successful", "user": user_data}), 200
    else:
        return jsonify({"message": "Registration failed"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response = requests.post(f"{event_url}/login", json=data)
    if response.status_code == 200:
        user_data = response.json()
        access_token = create_access_token(identity=user_data['id'])
        return jsonify({"access_token": access_token, "user": user_data}), 200
    else:
        return jsonify({"message": "Login failed"}), 401

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    # This route will be protected and only accessible with a valid JWT
    # The actual user data should be fetched from TigerGraph via the Events node
    return jsonify({"message": "Profile accessed successfully"}), 200

@app.route('/videos', methods=['GET'])
@jwt_required()
def videos():
    # This route will be protected and only accessible with a valid JWT
    # Fetch video list from Video_Server_Platform
    response = requests.get("http://localhost:5005/videos")
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"message": "Failed to fetch videos"}), 400

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()
    port = args.port
    app.run(host="0.0.0.0", port=port)
