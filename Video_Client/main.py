# Video_Client
from flask import Flask, Response, request, render_template, jsonify
from flask_socketio import SocketIO
from dotenv import load_dotenv
import sys
import requests
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
import json

load_dotenv()  

app = Flask(__name__)
url_dict = {}  # Initialize the URL dictionary to store video URLs
socketio = SocketIO(app, cors_allowed_origins='*')
bucket_name = os.getenv('S3_BUCKET_NAME')

@app.route('/')
def index():
    return "stream working"

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    global url_dict
    data = request.get_json()
    url_dict = data
    # print("DATA", data)
    base_url = request.host_url
    # print("base:", base_url)
    url_dict['base'] = base_url
    print("URL DICT", url_dict)

    # Create video_client Event
    requests.post(f"{url_dict['Events']}/create_video_client_event", json=url_dict)
    return("HI")

@app.route('/videos', methods=['GET', 'POST'])
def fetch_video_list():
    response = requests.get(f"{url_dict['video_server']}/videos")
    videos = response.json() if response.status_code == 200 else []
    return jsonify(videos)

@app.route('/thumbnail/<path:thumbnail_key>')
def get_thumbnail(thumbnail_key):
    response = requests.get(f"{url_dict['video_server']}/thumbnail/{thumbnail_key}")
    if response.status_code == 200:
        presigned_url = response.json().get('presigned_url')
        return jsonify({'presigned_url': presigned_url})
    else:
        return jsonify({'error': 'Failed to retrieve thumbnail'}), response.status_code

@app.route('/video/<video_key>')
def stream_video(video_key):
    # Request presigned URL from Video Server
    # Send video selection event
    try:
        requests.post(f"{url_dict['Events']}/video_selected_event", json={'video_key': video_key})
    except requests.exceptions.RequestException as e:
        print(f"Error sending video selection event: {e}")

    data = {'video_key': video_key}

    try:
        response = requests.post(f"{url_dict['video_server']}/presigned", json=data)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        
        if response.status_code == 200:
            try:
                response_json = response.json()
                presigned_url = response_json.get('presigned_url')
                if presigned_url:
                    # Proxy the video content from presigned URL to the client
                    def generate():
                        try:
                            with requests.get(presigned_url, stream=True) as r:
                                r.raise_for_status()
                                for chunk in r.iter_content(chunk_size=1024):
                                    if chunk:
                                        yield chunk
                        except requests.exceptions.RequestException as e:
                            print(f"Error streaming video: {e}")
                            yield b''  # Yield empty byte string to prevent stream interruption
                    return Response(generate(), mimetype='video/mp4')
                else:
                    print("No presigned URL received")
                    return jsonify({'error': 'No presigned URL received'}), 500
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                return jsonify({'error': 'Invalid JSON response from server'}), 500
        else:
            print(f"Failed to retrieve video. Status code: {response.status_code}")
            return jsonify({'error': 'Failed to retrieve video', 'status': response.status_code}), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error requesting presigned URL: {e}")
        return jsonify({'error': 'Error requesting presigned URL', 'details': str(e)}), 500

if __name__ == '__main__':
    port = 5001  # Default port
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    socketio.run(app, host='0.0.0.0', port=port)
