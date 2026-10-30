"""Picture REST API. The course stores pictures in a process-local list."""
import json
from pathlib import Path
from threading import RLock
from urllib.parse import urlparse

from flask import abort, jsonify, request
from . import app

with (Path(__file__).parent / 'data' / 'pictures.json').open() as source:
    data = json.load(source)
lock = RLock()


def picture_payload(expected_id=None):
    value = request.get_json()
    fields = ('pic_url', 'event_country', 'event_state', 'event_city', 'event_date')
    if not isinstance(value, dict) or type(value.get('id')) is not int or value['id'] < 1:
        abort(400, description='id must be a positive integer')
    if any(not isinstance(value.get(field), str) or not value[field].strip() for field in fields):
        abort(400, description='All picture fields must be nonempty strings')
    if urlparse(value['pic_url']).scheme not in ('http', 'https'):
        abort(400, description='pic_url must be an HTTP or HTTPS URL')
    if expected_id is not None and value['id'] != expected_id:
        abort(400, description='Body id must match the URL id')
    return {key: value[key] for key in ('id', *fields)}


@app.route('/health')
def health():
    return jsonify(status='OK'), 200


@app.route('/count')
def count():
    with lock:
        return jsonify(length=len(data)), 200


@app.route('/picture', methods=['GET'])
def get_pictures():
    with lock:
        return jsonify(data), 200


@app.route('/picture/<int:id>', methods=['GET'])
def get_picture_by_id(id):
    with lock:
        for picture in data:
            if picture['id'] == id:
                return jsonify(picture), 200
    return {'message': 'picture not found'}, 404


@app.route('/picture', methods=['POST'])
def create_picture():
    picture = picture_payload()
    with lock:
        if any(item['id'] == picture['id'] for item in data):
            return {'Message': f"picture with id {picture['id']} already present"}, 302
        data.append(picture)
    return jsonify(picture), 201


@app.route('/picture/<int:id>', methods=['PUT'])
def update_picture(id):
    picture = picture_payload(id)
    with lock:
        for index, item in enumerate(data):
            if item['id'] == id:
                data[index] = picture
                return jsonify(picture), 200
    return {'message': 'picture not found'}, 404


@app.route('/picture/<int:id>', methods=['DELETE'])
def delete_picture(id):
    with lock:
        for index, item in enumerate(data):
            if item['id'] == id:
                del data[index]
                return '', 204
    return {'message': 'picture not found'}, 404
