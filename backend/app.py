from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

@app.route('/')
def index():
    return send_from_directory(os.path.dirname(os.path.dirname(__file__)), 'index.html')

@app.route('/api/time-periods')
def get_time_periods():
    with open(os.path.join(DATA_DIR, 'time_periods_test.json'), 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

@app.route('/api/languages')
def get_languages():
    with open(os.path.join(DATA_DIR, 'languages.json'), 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

@app.route('/api/language-influences')
def get_language_influences():
    with open(os.path.join(DATA_DIR, 'language_influences.json'), 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

@app.route('/api/historical-boundaries')
def get_historical_boundaries():
    with open(os.path.join(DATA_DIR, 'historical_boundaries_test.json'), 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

@app.route('/api/historical-boundaries/<period_id>')
def get_historical_boundaries_by_period(period_id):
    with open(os.path.join(DATA_DIR, 'historical_boundaries.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)
        boundaries = [b for b in data['boundaries'] if b['period_id'] == period_id]
        return jsonify({'period_id': period_id, 'boundaries': boundaries})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
