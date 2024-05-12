import requests
from flask import Flask, render_template, Response
import threading
import time

app = Flask(__name__)

STREAMING_SERVERS = ['http://localhost:5001', 'http://localhost:5002']

class VideoStreamer:
    def __init__(self):
        self.current_server_index = 0
        self.lock = threading.Lock()
        self.responses = [None, None]
        self.current_server_url = STREAMING_SERVERS[self.current_server_index]  # Store current server URL
        self.playtime = 0  # Variable to store video playtime
        self.fetch_chunks()

    def fetch_chunks(self):
        def fetch_from_server(server_url, index):
            try:
                self.responses[index] = requests.get(server_url + '/video_feed', stream=True)
            except requests.exceptions.RequestException:
                self.responses[index] = None

        threads = []
        for i, server_url in enumerate(STREAMING_SERVERS):
            thread = threading.Thread(target=fetch_from_server, args=(server_url, i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()


    def get_video_stream(self):
        while True:
            with self.lock:
                current_response = self.responses[self.current_server_index]
                if current_response:
                    current_playtime = time.time() - self.playtime  # Calculate current playtime
                    for chunk in current_response.iter_content(chunk_size=512):
                        yield chunk
                        if time.time() - self.playtime > current_playtime:
                            # Update playtime after yielding a chunk
                            self.playtime = time.time()
                else:  # If current server is not available
                    self.switch_server()
                    continue  # Continue streaming from the next server without waiting

                next_server_index = (self.current_server_index + 1) % len(STREAMING_SERVERS)
                next_response = self.responses[next_server_index]
                if next_response:  # If the next server is available
                    self.current_server_index = next_server_index
                    self.current_server_url = STREAMING_SERVERS[self.current_server_index]  # Update current server URL
                    self.playtime = time.time()  # Update playtime after switching servers

    def switch_server(self):
        with self.lock:
            next_server_index = (self.current_server_index + 1) % len(STREAMING_SERVERS)
            for i in range(len(STREAMING_SERVERS)):
                index = (next_server_index + i) % len(STREAMING_SERVERS)
                if self.responses[index] is not None:  # Find the first available server
                    self.current_server_index = index
                    self.current_server_url = STREAMING_SERVERS[self.current_server_index]  # Update current server URL
                    return

            # If none of the servers are available, reset to the first server
            self.current_server_index = 0
            self.current_server_url = STREAMING_SERVERS[self.current_server_index]  # Update current server URL




video_streamer = VideoStreamer()

@app.route('/')
def index():
    current_server_url = video_streamer.current_server_url
    return render_template('index.html', current_server_url=current_server_url)

@app.route('/current_server_url')
def current_server_url():
    return video_streamer.current_server_url


@app.route('/video_feed')
def video_feed():
    return Response(video_streamer.get_video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
