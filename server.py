from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()
PORT = int(os.getenv('SERVER_PORT', 3000))

app = Flask(__name__)
CORS(app)

# Налаштування Google Cloud Storage
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account-key.json'  # Шлях до вашого JSON-ключа
BUCKET_NAME = 'my-robot-images'  # Назва вашого бакета
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

ROBOTS_FILE = 'robots.json'
if not os.path.exists(ROBOTS_FILE):
    with open(ROBOTS_FILE, 'w') as f:
        json.dump([], f, indent=2)

@app.route('/robots', methods=['GET'])
def get_robots():
    with open(ROBOTS_FILE, 'r') as f:
        robots = json.load(f)
    return jsonify(robots)

@app.route('/add_robot', methods=['POST'])
def add_robot():
    author = request.form.get('author')
    name = request.form.get('name')
    description = request.form.get('description')
    files = request.files.getlist('images')

    if not author or not name or not description or not files:
        return jsonify({'error': 'Missing fields or files'}), 400

    image_urls = []
    for file in files:
        if file and (file.filename.endswith('.jpg') or file.filename.endswith('.jpeg') or file.filename.endswith('.png')):
            # Завантаження файлу в Cloud Storage
            blob = bucket.blob(f"images/{file.filename}")
            blob.upload_from_file(file, content_type=file.content_type)
            blob.make_public()  # Робимо файл публічним
            image_urls.append(blob.public_url)

    # Оновлення robots.json
    with open(ROBOTS_FILE, 'r') as f:
        robots = json.load(f)

    new_robot = {
        'author': author,
        'name': name,
        'description': description,
        'images': image_urls,
        'price': request.form.get('price', 'Ціна не вказана')
    }
    robots.append(new_robot)

    with open(ROBOTS_FILE, 'w') as f:
        json.dump(robots, f, indent=2)

    return jsonify({'message': 'Robot added successfully'}), 200

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