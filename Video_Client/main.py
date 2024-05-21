from flask import Flask, Response
import sys
import requests


app = Flask(__name__)

@app.route('/')
def index():
    return("stream working")

@app.route('/video_feed')
def video_feed():
    def generate():
        response = requests.get('http://localhost:8080/')  # Replace with the actual URL of your server
        video_url = response.text
        print(f'Video URL: {video_url}')  # Print the video URL
        video_response = requests.get(video_url, stream=True)
        print(f'Video response status code: {video_response.status_code}')  # Print the status code of the video response

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
