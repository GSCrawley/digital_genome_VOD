# UI main.py
import requests
import time
import threading
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
url_dict = None  # Initialize url_dict globally
primary_url = None
backup_url = None
current_url = None
lock = threading.Lock()


def check_primary_availability():
    global primary_url, backup_url, current_url
    while True:
        with lock:
            try:
                response = requests.get(primary_url)
                if response.status_code != 200:
                    current_url = backup_url
                else:
                    current_url = primary_url
            except requests.ConnectionError:
                current_url = backup_url
        # Sleep for some time before checking again
        time.sleep(5)

# Start the thread to continuously check primary URL availability
check_thread = threading.Thread(target=check_primary_availability)
check_thread.daemon = True
check_thread.start()

# Define a route to display the video list nd handle video selection
@app.route('/setup', methods=['GET', 'POST'])
def setup():
    global url_dict, primary_url, backup_url, current_url
    data = request.get_json()
    url_dict = data
    primary_url = url_dict['video_client'][0]
    backup_url = url_dict['video_client'][1]
    current_url = primary_url  # Initially set current URL to primary URL
    return "hi"

@app.route('/')
def index():
    global current_url
    response = requests.get(f"{current_url}/videos")
    videos = response.json() if response.status_code == 200 else []
    return render_template('video_list.html', videos=videos)

@app.route('/select_video', methods=['POST'])
def select_video():
    selected_video = request.form['video']
    # Redirect to video feed route with selected video key
    return redirect(url_for('video_feed', video_key=selected_video))

@app.route('/video_feed/<video_key>', methods=['GET'])
def video_feed(video_key):
    global current_url
    try:
        response = requests.get(f"{current_url}/video/{video_key}", stream=True)
        print(current_url)
        if response.status_code == 200:
            return Response(response.iter_content(chunk_size=1024), content_type='video/mp4')
    except requests.ConnectionError:
        pass  # Connection to current URL failed, switch to backup URL
    
    # If connection to current URL failed, try to fetch from backup URL
    try:
        response = requests.get(f"{backup_url}/video/{video_key}", stream=True)
        print(backup_url)
        if response.status_code == 200:
            return Response(response.iter_content(chunk_size=1024), content_type='video/mp4')
    except requests.ConnectionError:
        pass  # Both primary and backup URLs are unavailable
    
    return jsonify({'error': 'Failed to retrieve video'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
