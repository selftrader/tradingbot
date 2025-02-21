# ui/app.py

from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template("index.html")

def run_ui():
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
