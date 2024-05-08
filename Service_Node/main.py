from flask import Flask, jsonify
import requests 

app = Flask(__name__)

@app.route('/')
def home():
    return('hello world')

@app.route('/video_url', methods=['POST','GET'])
def index():
    response = requests.post('http://127.0.0.1:8080/')

    public_url = response.json()
    print(public_url)

    return jsonify(public_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)