# Video Client Server
from flask import Flask, Response, request, render_template, jsonify
import sys
import requests
import boto3

app = Flask(__name__)
url_dict = {}  # Initialize the URL dictionary to store video URLs

@app.route('/')
def index():
    return "stream working"

@app.route('/setup', methods=['GET','POST'])
def setup():
    global url_dict
    data = request.get_json()
    url_dict = data
    print("URLs:", url_dict)
    return "Setup successful"

def generate_presigned_url(bucket_name, video_key):
    s3_client = boto3.client('s3')
    presigned_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': video_key},
        ExpiresIn=3600
    )
    return presigned_url

@app.route('/video/<video_key>')
def get_video(video_key):
    bucket_name = 'gidvidbucket'
    presigned_url = generate_presigned_url(bucket_name, video_key) # Function to generate presigned URL for the selected video
    return render_template('video_player.html', video_url=presigned_url)

@app.route('/get_presigned_url', methods=['POST'])
def get_presigned_url():
    video_key = request.json.get('video_key')  # Assuming the video key is sent in the request JSON
    if not video_key:
        return jsonify({'error': 'Video key is required in the request'}), 400

    presigned_url = generate_presigned_url(bucket_name, video_key)  # Using the generate_presigned_url function

    return jsonify({'presigned_url': presigned_url})

@app.route('/video_feed', methods=['POST'])
def video_feed():
    selected_video = request.json.get('selected_video')  # Get the selected video from the User Interface
    if selected_video not in url_dict:
        return "Selected video not found in the list", 404

    video_url = url_dict[selected_video]
    print(f'Selected Video URL: {video_url}')  # Print the selected video URL
    video_response = requests.get(video_url, stream=True)
    print(f'Video response status code: {video_response.status_code}')  # Print the status code of the video response

    def generate():
        if video_response.status_code == 200:
            for chunk in video_response.iter_content(chunk_size=1024):
                if not chunk:
                    break
                yield chunk
        else:
            print(f'Error fetching video: {video_response.status_code}')
            yield b'Error fetching video'

    return Response(generate(), mimetype='video/mp4')

if __name__ == '__main__':
    port = 5001  # Default port
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port)