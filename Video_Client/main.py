# Video Client Server
from flask import Flask, Response, request, render_template, jsonify
from flask_socketio import SocketIO
from dotenv import load_dotenv
import sys
import requests
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os

load_dotenv()  

app = Flask(__name__)
socketio = SocketIO(app)
url_dict = {}  # Initialize the URL dictionary to store video URLs

bucket_name = os.getenv('S3_BUCKET_NAME')

@socketio.on('play')
def handle_play_event(data):
    print('Video is playing at', data['time'])

@socketio.on('pause')
def handle_pause_event(data):
    print('Video is paused at', data['time'])

@socketio.on('timeupdate')
def handle_timeupdate_event(data):
    print('Video time updated:', data['time'])

@app.route('/')
def index():
    return "stream working"

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    global url_dict
    data = request.get_json()
    url_dict = data
    print("DATA", data)
    return "hi"

@app.route('/videos', methods=['GET', 'POST'])
def fetch_video_list():
    response = requests.get(f"{url_dict['video_server']}/videos")
    videos = response.json() if response.status_code == 200 else []
    return videos

@app.route('/video/<video_key>')
def stream_video(video_key):
    # Request presigned URL from Video Server
    data = video_key
    response = requests.post(f"{url_dict['video_server']}/presigned", json=data)
    if response.status_code == 200:
        presigned_url = response.json().get('presigned_url')
        # Proxy the video content from presigned URL to the client
        def generate():
            with requests.get(presigned_url, stream=True) as r:
                for chunk in r.iter_content(chunk_size=1024):
                    yield chunk
        return Response(generate(), mimetype='video/mp4')
    else:
        return jsonify({'error': 'Failed to retrieve video'}), response.status_code
# The following route will be used when we add video upload capability:

# @app.route('/receive_video', methods=['POST'])
# def receive_video():
#     if 'video' not in request.files:
#         return jsonify({'error': 'No video file part'}), 400

#     video_file = request.files['video']
    
#     if video_file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     if video_file and allowed_file(video_file.filename):
#         # Here you would typically process the file and then upload it to S3
#         # For example, you could save the file temporarily and then use boto3 to upload
#         # Or you could stream the file directly to S3 without saving it locally

#         # ... (Your S3 upload logic)

#         return jsonify({'message': 'Video successfully received'}), 200
#     else:
#         return jsonify({'error': 'Invalid file type'}), 400

# def allowed_file(filename):
#     # Check if the file has one of the allowed extensions
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define the set of allowed file extensions (e.g., 'mp4', 'avi', 'mov', etc.)
# ALLOWED_EXTENSIONS = set(['mp4', 'avi', 'mov'])


if __name__ == '__main__':
    port = 5001  # Default port
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    socketio.run(app, host='0.0.0.0', port=port)