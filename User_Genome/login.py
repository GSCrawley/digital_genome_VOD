from flask import jsonify, request
import requests
from flask_jwt_extended import create_access_token

def login_data(request, cloud_url):
    print("Hello!")
    email = request.json.get('email')
    password = request.json.get('password')
    url = f'{cloud_url}/login'
    data = {'email': email, 'password': password}
    response = requests.post(url, json=data)
    response = response.json()
    if response == {'User': []}:
        print("RESULT: ", response)
        return jsonify({"status":"error", "message": "Invalid email or password"}), 401
    v_id = response['User'][0]['v_id']
    access_token = create_access_token(identity=v_id)
    return jsonify({'access_token': access_token}), 200