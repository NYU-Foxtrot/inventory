#Given the id of the product
# When I use "read the product"
# Then I get a list of the inventory records containing that product id
# sum up the "quantity" field.


import logging
from flask import Flask, jsonify
from models import  DataValidationError, ProductStatus, Inventory
# Create Flask application
app = Flask(__name__)

# Status Codes
HTTP_200_OK = 200
HTTP_404_NOT_FOUND = 404

@app.route('/inventory/count/<int:id>', methods=['GET'])
def list_resources(id):
	# return a list of Inventory

	find_by_id_records = Inventory.findAll_by_id(id)
	
    if find_by_id_records
        quantity_sum = sum([ record.quantity for record in find_by_id_records])
        message = {'quantity_sum' : quantity_sum}
        return_code = HTTP_200_OK
    else:
        message = {'error' : 'Fetch inventory records error'}
        return_code = HTTP_404_NOT_FOUND

    return jsonify(message), return_code 