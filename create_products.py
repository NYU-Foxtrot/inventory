import logging
from flask import Flask, Response, jsonify, request, json, make_response
from models import Product

app = Flask(__name__)

@app.route('/inventory', methods=['POST'])
def create_products():
	app.logger.info('Products creating requested')
	payload = request.get_json()
	product = Product()
	product.deserialize(payload)
	product.save()
	app.logger.info('Created Product with id: {}'.format(product.id))
	response = make_response(jsonify(product.serialize()), status.HTTP_201_CREATED)
	response.headers['Location'] = product.self_url()
	return response