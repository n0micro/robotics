from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv

load_dotenv()
PORT = int(os.getenv('SERVER_PORT', 3000))

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ROBOTS_FILE = 'robots.json'
if not os.path.exists(ROBOTS_FILE):
    with open(ROBOTS_FILE, 'w') as f:
        json.dump([], f, indent=2)

@app.route('/robots', methods=['GET'])
def get_robots():
    with open(ROBOTS_FILE, 'r') as f:
        robots = json.load(f)
    return jsonify(robots)

@app.route('/static_images/<path:filename>')
def serve_static_images(filename):
    return send_from_directory('static_images', filename)

@app.route('/')
@app.route('/index.html')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/index.css')
def serve_css():
    return send_from_directory('.', 'index.css')

@app.route('/index.js')
def serve_js():
    return send_from_directory('.', 'index.js')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
