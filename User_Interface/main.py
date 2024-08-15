from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from flask_socketio import SocketIO, emit
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
import requests
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Ensure you have a secret key
socketio = SocketIO(app, cors_allowed_origins='*')

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'test'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token_cookie'
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

jwt = JWTManager(app)

url_dict = None  # Initialize url_dict globally
primary_url = None
current_url = None

def check_primary_availability():
    global primary_url, current_url
    while True:
        print(f"Checking server availability: {current_url}")
        try:
            response = requests.get(current_url, timeout=3)
            if response.status_code != 200:
                print(f"Server {current_url} is down, attempting switch.")
                switch_server()
            else:
                print(f"Server {current_url} is up and running.")
        except requests.ConnectionError:
            print(f"Connection error with server {current_url}, switching...")
            switch_server()
        time.sleep(5)

def switch_server():
    global current_url
    print("Attempting to switch servers...")
    socketio.emit('server_switch_start')
    try:
        response = requests.get(f"{url_dict['SWM']}/recover", timeout=3)
        response_json = response.json()
        new_url = response_json
        print(f"Received new server URL: {new_url}")
        if new_url and new_url != current_url:
            current_url = new_url
            print(f"Emitting server_switch event with new URL: {current_url}")
            socketio.emit('server_switch', {'new_server_url': current_url})
            print(f"Switched to new server: {current_url}")
        else:
            print("Failed to switch servers: No new server URL provided or URL is the same.")
    except requests.RequestException as e:
        print(f"Error switching servers: {e}")

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    global url_dict, primary_url, current_url
    data = request.get_json()
    url_dict = data
    primary_url = url_dict['video_client'][0]
    current_url = primary_url
    return "hi"

@app.route('/')
def index():
    global current_url
    response = requests.get(f"{current_url}/videos")
    print("Response from video service:", response.json())
    items = response.json() if response.status_code == 200 else []
    videos_with_thumbnails = [{'name': item.get('name'), 'video': item.get('video'), 'thumbnail': item.get('thumbnail')} for item in items if isinstance(item, dict)]
    threading.Thread(target=check_primary_availability, daemon=True).start()
    return render_template('video_list.html', videos=videos_with_thumbnails)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {'username': request.form.get('username'), 'email': request.form.get('email'), 'password': request.form.get('password')}
        response = requests.post(f"{url_dict['User_Genome']}/register", json=data)
        if response.status_code == 200:
            return redirect('/')
        else:
            return render_template('register.html', error="Registration failed")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {'email': request.form.get('email'), 'password': request.form.get('password')}
        response = requests.post(f"{url_dict['User_Genome']}/login", json=data)
        if response.status_code == 200:
            user_identity = response.json()['user_identity']
            access_token = create_access_token(identity=user_identity)
            resp = redirect('/')
            resp.set_cookie('access_token_cookie', access_token)
            return resp
    return render_template('login.html')

@app.route('/thumbnail/<thumbnail_key>')
def get_thumbnail(thumbnail_key):
    global current_url
    try:
        response = requests.get(f"{current_url}/thumbnail/{thumbnail_key}", timeout=5)
        if response.status_code == 200:
            presigned_url = response.json().get('presigned_url')
            if presigned_url:
                return redirect(presigned_url)
        return redirect(url_for('static', filename='default_thumbnail.png'))
    except Exception as e:
        app.logger.error(f"Error retrieving thumbnail: {thumbnail_key}. Error: {str(e)}")
        return redirect(url_for('static', filename='default_thumbnail.png'))

@app.route('/select_video', methods=['POST'])
@jwt_required()
def select_video():
    current_user = get_jwt_identity()
    print("CURRENT USER: ", current_user)
    selected_video = request.form['video']
    video_selection_event(selected_video, current_user)
    return redirect(url_for('watch_video', video_key=selected_video))

@app.route('/video_feed/<video_key>', methods=['GET'])
def video_feed(video_key):
    global current_url
    # threading.Thread(target=check_primary_availability, daemon=True).start()
    video_feed_url = f"{current_url}/video/{video_key}"
    try:
        response = requests.get(video_feed_url, stream=True)
        if response.status_code == 200:
            return Response(response.iter_content(chunk_size=1024), content_type='video/mp4')
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred", 500

@app.route('/watch/<video_key>')
def watch_video(video_key):
    global current_url
    video_feed_url = url_for('video_feed', video_key=video_key)
    return render_template('video_player.html', video_url=video_feed_url, current_server_url=current_url)

def video_selection_event(selected_video, current_user):
    data = {"selected_video": selected_video, "current_user": current_user}
    response = requests.post(f"{url_dict['Events']}/video_selected_event", json=data)


@app.route('/test')
def test():
    return('tested')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

