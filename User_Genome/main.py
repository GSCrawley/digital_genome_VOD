import config
# import openai
from flask import Flask, jsonify, request, session, g
from flask_jwt_extended import JWTManager, jwt_required, \
                               create_access_token
import requests, names, random, threading, uuid, json
import argparse

from register import register_data
from login import login_data
from profile import profile_data

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY # change this to a random string in production
cloud_url = "http://localhost:8080"
jwt = JWTManager(app)


# openai.api_key = config.openai_key

class User:
    def __init__(self):
        self.unique_id = str(uuid.uuid4())
        self.dummy_id = self.unique_id[:2]
        self.first_name = names.get_first_name(gender=self.gender)
        self.last_name = names.get_last_name()
        self.username = 'test'
        self.password = f'test{self.dummy_id}'
        self.email = f'test{self.dummy_id}@test.com'
        self.join_date = self._generate_date()


    def _generate_date(self):
        return str(random.randint(1922, 2010))

    def display_info(self):
        print("First Name:", self.first_name)
        print("Last Name:", self.last_name)
        print("Gender:", self.gender)
        print("Username:", self.username)
        print("Password:", self.password)
        print("Email:", self.email)
        print("Join Date:", self.join_date)

@app.route('/', methods = ['GET'])
def home():
    if(request.method == 'GET'):
        data = "hello Class!"
        return jsonify({'data': data})

@app.route('/register', methods=['POST'])
def register():
    new_user_id = register_data(request)
    event_url = get_event_server()
    event_url = event_url['url']
    event_url = f'{event_url}/event-user-register'
    data = {'user_id': new_user_id}
    print("event", event_url)
    event_response = requests.post(event_url, json=data)
    return('hi')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_data(request, cloud_url)

@app.route('/profile', methods=['GET', 'POST'])
@jwt_required()
def profile():
    user = User()
    return profile_data(cloud_url, user)

def get_event_server():
    event_url = f'{cloud_url}/event_server'
    response = requests.get(event_url)
    return response.json()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()
    port = args.port
    app.run(host="0.0.0.0", port=port)