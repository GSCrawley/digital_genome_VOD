import config
from flask import Flask, jsonify, request, render_template, redirect, url_for, make_response
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies
import requests

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
jwt = JWTManager(app)

event_url = "http://localhost:5006"  # Assuming the Events node is running on localhost:5006

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        response = requests.post(f"{event_url}/login", json=data)
        if response.status_code == 200:
            user_data = response.json()
            access_token = create_access_token(identity=user_data['id'])
            resp = make_response(redirect(url_for('profile')))
            resp.set_cookie('access_token_cookie', access_token)
            return resp
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        response = requests.post(f"{event_url}/register", json=data)
        if response.status_code == 200:
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="Registration failed")
    return render_template('register.html')

@app.route('/profile')
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    # Fetch user data from TigerGraph via the Events node
    response = requests.get(f"{event_url}/user/{current_user}")
    if response.status_code == 200:
        user_data = response.json()
        return render_template('profile.html', user=user_data)
    else:
        return jsonify({"message": "Failed to fetch user data"}), 400

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    unset_jwt_cookies(resp)
    return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
