from flask import Flask, Response
import sys

app = Flask(__name__)

# Replace 'video.mp4' with the code to get the video from the s3 bucket
VIDEO_PATH = f"https://gidvidbucket.s3.amazonaws.com/the_divine_proportion.mp4"

@app.route('/')
def index():
    return("stream working")

@app.route('/video_feed')
def video_feed():
    def generate():
        with open(VIDEO_PATH, 'rb') as video_file:
            while True:
                data = video_file.read(1024)
                if not data:
                    break
                yield data
    return Response(generate(), mimetype='video/mp4')

if __name__ == '__main__':
    port = 5001  # Default port
    if len(sys.argv) > 1:
        port = int(sys.argv[1])