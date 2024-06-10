from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('server_ui.html')

@app.route('/fail_primary', methods=['POST'])
def fail_primary():
    requests.post('http://localhost:5001/fail')  # Simulating failure of primary server
    return redirect(url_for('index'))

@app.route('/fail_backup', methods=['POST'])
def fail_backup():
    requests.post('http://localhost:5002/fail')  # Simulating failure of backup server
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
