# We could read the record from URL /inventory/all

import logging
from flask import Flask, jsonify
from models import  DataValidationError, ProductStatus, Inventory
# Create Flask application
app = Flask(__name__)

# Status Codes
HTTP_200_OK = 200
HTTP_404_NOT_FOUND = 404

@app.route('/inventory/all', methods=['GET'])
def list_resources():
	# return a list of Inventory

	all_inventory_records = Inventory.all()
	
    if all_inventory_records:
        message = [ record.serialize() for record in all_inventory_records]
        return_code = HTTP_200_OK
    else:
        message = {'error' : 'Fetch inventory records error'}
        return_code = HTTP_404_NOT_FOUND

    return jsonify(message), return_code 