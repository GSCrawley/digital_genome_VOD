# UI main.py
import requests
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for

app = Flask(__name__)

VIDEO_SERVER_PLATFORM_URL = 'http://localhost:5005'
VIDEO_CLIENT_URL = 'http://localhost:5001'

# Define a route to display the video list and handle video selection
@app.route('/')
def index():
     # Fetch the list of videos from Video_Server_Platform
    response = requests.get(f'{VIDEO_SERVER_PLATFORM_URL}/videos')
    videos = response.json() if response.status_code == 200 else []
    
    return render_template('video_list.html', videos=videos)

# Define a route to handle the selection of a video and generate a presigned URL
@app.route('/select_video', methods=['POST'])
def select_video():
    selected_video = request.form['video']
    # Generate presigned URL for the selected video by requesting it from the Video Client
    response = requests.get(f'{VIDEO_CLIENT_URL}/video/{selected_video}')
    
    if response.status_code == 200:
        # Extract the presigned url from the response
        presigned_url = response.json().get('presigned_url')
        if presigned_url:
            # Render the video player template with the presigned URL
            return render_template('video_player.html', video_url=presigned_url)
        else:
            # If the 'presigned_url' key is not in the response, handle the error
            error_message = response.json().get('error', 'Unknown error.')
            return jsonify({'error': error_message}), 500
    else:
        # If the response status code is not 200, handle the error
        return jsonify({'error': 'Failed to generate presigned URL'}), response.status_code


@app.route('/video_feed/<video_key>', methods=['GET'])
def video_feed(video_key):
    # Request presigned URL from Video Client
    response = requests.get(f'{VIDEO_CLIENT_URL}/video/{video_key}')
    if response.status_code == 200:
        presigned_url = response.json().get('presigned_url')
        return render_template('video_player.html', video_url=presigned_url)
    else:
        return jsonify({'error': 'Failed to retrieve video'}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)