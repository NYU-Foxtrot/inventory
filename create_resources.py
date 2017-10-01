import logging
from flask import Flask, Response, jsonify, request, json, make_response
from models import Resource

app = Flask(__name__)

@app.route('/inventory', methods=['POST'])
def create_resources():
	app.logger.info('Resources creating requested')
	payload = request.get_json()
	resource = Resource()
	resource.deserialize(payload)
	resource.save()
	app.logger.info('Created Resource with id: {}'.format(resource.id))
	response = make_response(jsonify(resource.serialize()), status.HTTP_201_CREATED)
	response.headers['Location'] = resource.self_url()
	return response