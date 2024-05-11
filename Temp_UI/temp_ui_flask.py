from flask import Flask, render_template, jsonify, request
import requests 

app = Flask(__name__)

@app.route('/')
def index():
    # Fetch list of videos from another service or endpoint
    video_list_response = requests.get('http://127.0.0.1:8082/list_videos')
    video_list = video_list_response.json().get('urls', [])
    return render_template('index.html', video_list=video_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)