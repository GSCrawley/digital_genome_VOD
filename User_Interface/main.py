# UI
import requests
import time
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
url_dict = None  # Initialize url_dict globally
socketio = SocketIO(app, cors_allowed_origins='*')
primary_url = None
current_url = None

def check_primary_availability():
    global primary_url, current_url
    try:
        response = requests.get(current_url)
        if response.status_code != 200:
            # Emit server_switch_start event
            socketio.emit('server_switch_start')
            # If the primary URL is down, get the new URL from the SWM
            response = requests.get(f"{url_dict['SWM']}/recover")
            new_url = response.json()  # Assume this returns the new URL
            if new_url != current_url:
                # Update the current_url and notify the clients
                current_url = new_url
                socketio.emit('server_switch', {'new_server_url': current_url})
        else:
            # If the primary URL is up, ensure it is set as the current URL
            current_url = primary_url
    except requests.ConnectionError:
        # Emit server_switch_start event
        socketio.emit('server_switch_start')
        # If there is a connection error, get the new URL from the SWM
        response = requests.get(f"{url_dict['SWM']}/recover")
        new_url = response.json()  # Assume this returns the new URL
        if new_url != current_url:
            # Update the current_url and notify the clients
            current_url = new_url
            socketio.emit('server_switch', {'new_server_url': current_url})
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
    print("Response from video service:", response.json())
    items = response.json() if response.status_code == 200 else []
    # Assuming `items` is now a list of dictionaries with 'name', 'video', and 'thumbnail' keys
    videos_with_thumbnails = [
        {
            'name': item.get('name'),  # Assuming each item has a 'name'
            'video': item.get('video'),  # Assuming each item has a 'video' URL or identifier
            'thumbnail': item.get('thumbnail')  # Assuming each item has a 'thumbnail' URL or identifier
        } for item in items if isinstance(item, dict)
    ]

    return render_template('video_list.html', videos=videos_with_thumbnails)

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
            # resp.headers['Accept-Ranges'] = 'bytes'
            # resp.headers['Content-Range'] = response.headers.get('Content-Range', '*')
            # return resp

    except Exception as e:  # Catch all exceptions
        print(f"An error occurred: {e}")
        return "An error occurred", 500 

@app.route('/watch/<video_key>')
def watch_video(video_key):
    global current_url
    video_feed_url = url_for('video_feed', video_key=video_key)
    return render_template('video_player.html', video_url=video_feed_url, current_server_url=current_url)


def video_selection_event(selected_video):
    # send selected video event
    response = requests.post(f"{url_dict['Events']}/video_selected_event", json=selected_video)
    return response

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
