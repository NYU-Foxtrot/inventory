import logging
from flask import Flask, jsonify
from models import Product, DataValidationError

# Create Flask application
app = Flask(__name__)

# Status Codes
HTTP_200_OK = 200
HTTP_404_NOT_FOUND = 404

@app.errorhandler(404)
def not_found(error):
    """ Handles Pets that cannot be found """
    return jsonify(status=404, error='Not Found', message=error.message), 404

@app.route('/products/<int:id>', methods=['GET'])
def get_products(id):
    product = Product.find(id)
    if product:
        message = product.serialize()
        return_code = HTTP_200_OK
    else:
        message = {'error' : 'Product with id: %s was not found' % str(id)}
        return_code = HTTP_404_NOT_FOUND

    return jsonify(message), return_code