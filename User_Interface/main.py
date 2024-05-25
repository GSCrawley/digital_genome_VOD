# UI main.py
import requests
from flask import Flask, render_template, Response, request

app = Flask(__name__)

# Define a route to display the video list and handle video selection
@app.route('/')
def index():
    # Fetch the list of videos from Video_Server_Platform (assumed to be stored in VIDEO_LIST)
    videos = []  # Example video list
    
    return render_template('video_list.html', videos=videos)

# Define a route to handle the selection of a video and generate a presigned URL
@app.route('/select_video', methods=['POST'])
def select_video():
    selected_video = request.form['video']
    # Generate presigned URL for the selected video (you can implement this part)
    presigned_url = generate_presigned_url(selected_video)  # Implement this function
    
    return render_template('video_player.html', video_url=presigned_url)

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
    app.run(host='0.0.0.0', port=5000)