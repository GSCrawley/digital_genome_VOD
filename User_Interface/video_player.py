from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('video_player.html')

@app.route('/play', methods=['POST'])
def play():
    # Code to handle the play action
    return 'Play action triggered'

@app.route('/pause', methods=['POST'])
def pause():
    # Code to handle the pause action
    return 'Pause action triggered'

@app.route('/stop', methods=['POST'])
def stop():
    # Code to handle the stop action
    return 'Stop action triggered'

@app.route('/rewind', methods=['POST'])
def rewind():
    # Code to handle the rewind action
    return 'Rewind action triggered'

@app.route('/fast-forward', methods=['POST'])
def fast_forward():
    # Code to handle the fast-forward action
    return 'Fast-forward action triggered'

if __name__ == '__main__':
    app.run()