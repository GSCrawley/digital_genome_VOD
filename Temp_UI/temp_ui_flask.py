from flask import Flask, render_template
import requests 

app = Flask(__name__)

@app.route('/')
def index():
    response = requests.post('http://127.0.0.1:8082/video_url')
    print(response.json())
    public_url = response.json()
    return render_template('index.html', public_url=public_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)