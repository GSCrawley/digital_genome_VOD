# UI
import requests
import time
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
url_dict = None  # Initialize url_dict globally
socketio = SocketIO(app, cors_allowed_origins='*')
primary_url = None
current_url = None

def check_primary_availability():
    global primary_url, current_url
    test = requests.get(f"{url_dict['SWM']}/recover")
    try:
        response = requests.get(current_url)
        if response.status_code != 200:
            response = requests.get(f"{url_dict['SWM']}/recover")
            current_url = response.json()
        else:
            current_url = primary_url
    except requests.ConnectionError:
        response = requests.get(f"{url_dict['SWM']}/recover")
        current_url = response.json()
        # Sleep for some time before checking again
        time.sleep(1)


@app.route('/setup', methods=['GET', 'POST'])
def setup():
    global url_dict, primary_url, current_url
    data = request.get_json()
    url_dict = data
    primary_url = url_dict['video_client'][0]
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
    return redirect(url_for('watch_video', video_key=selected_video))

@app.route('/video_feed/<video_key>', methods=['GET'])
def video_feed(video_key):
    global current_url
    check_primary_availability()
    video_feed_url = f"{current_url}/video/{video_key}"
    try:
        response = requests.get(video_feed_url, stream=True)
        print("NOW STREAMING FROM:", current_url)
        if response.status_code == 200:
            return Response(response.iter_content(chunk_size=1024), content_type='video/mp4')
    except Exception as e:  # Catch all exceptions
        print(f"An error occurred: {e}")
        return "An error occurred", 500  # Return a 500 error if an exception is raised
    
    # return jsonify({'error': 'Failed to retrieve video'}), 500

@app.route('/watch/<video_key>')
def watch_video(video_key):
    global current_url
    video_feed_url = url_for('video_feed', video_key=video_key)
    return render_template('video_player.html', video_url=video_feed_url, current_server_url=current_url)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)