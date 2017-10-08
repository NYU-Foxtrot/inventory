# Copyright 2017 NYU-FOXTROT. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Inventory Store Service

Paths:
------
GET /inventories - Returns a list all of the Inventories
GET /inventories/{id} - Returns the Inventory with a given id number
POST /inventories - creates a new Inventory record in the database
PUT /inventories/{id} - updates a Inventory record in the database
DELETE /inventories/{id} - deletes a Inventory record in the database
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response
from flask_api import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound
from models import Inventory, DataValidationError

# Create Flask application
app = Flask(__name__)

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')


######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)


@app.errorhandler(400)
def bad_request(error):
    """ Handles bad requests with 400_BAD_REQUEST """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=400, error='Bad Request', message=message), 400


@app.errorhandler(404)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=404, error='Not Found', message=message), 404


@app.errorhandler(405)
def method_not_supported(error):
    """ Handles unsupported HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=405, error='Method not Allowed', message=message), 405


@app.errorhandler(415)
def mediatype_not_supported(error):
    """ Handles unsupported media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=415, error='Unsupported media type', message=message), 415


@app.errorhandler(500)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=500, error='Internal Server Error', message=message), 500


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Root URL response """
    return jsonify(name='Inventory Demo REST API Service',
                   version='1.0',
                   paths=url_for('list_inventories', _external=True)
                   ), status.HTTP_200_OK


######################################################################
# LIST ALL INVENTORIES
######################################################################
@app.route('/inventories', methods=['GET'])
def list_inventories():
    """ Returns all of the Inventories """
    inventories = []
    # quantity = request.args.get('quantity')
    # status = request.args.get('status')
    # name = request.args.get('name')
    # if quantity:
    #     inventories = Inventory.find_by_quantity(quantity)
    # # here find_by_status() has some problem
    # elif status:
    #     inventories = Inventory.find_by_status(status)
    # elif name:
    #     inventories = Inventory.find_by_name(name)
    # else:
    #     inventories = Inventory.all()
    inventories = Inventory.all()

    results = [inventory.serialize() for inventory in inventories]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# READ AN INVENTORY
######################################################################
@app.route('/inventories/<int:inventory_id>', methods=['GET'])
def get_inventories(inventory_id):
    """
    Retrieve a single Inventory

    This endpoint will return a Inventory based on it's id
    """
    inventory = Inventory.find(inventory_id)
    if not inventory:
        raise NotFound("Pet with id '{}' was not found.".format(inventory_id))
    return make_response(jsonify(inventory.serialize()), status.HTTP_200_OK)


######################################################################
# CREATE AN INVENTORY
######################################################################
@app.route('/inventories', methods=['POST'])
def create_inventories():
    """
    Creates a Inventory
    This endpoint will create a Inventory based the data in the body that is posted
    """


######################################################################
# UPDATE AN EXISTING INVENTORY
######################################################################
@app.route('/inventories/<int:inventory_id>', methods=['PUT'])
def update_inventories(inventory_id):
    """
    Update a Inventory

    This endpoint will update a Inventory based the body that is posted
    """
    inventory = Inventory.find(inventory_id)
    if not inventory:
        raise NotFound("Inventory with id '{}' was not found.".format(inventory_id))
    inventory.deserialize(request.get_json())
    inventory.id = inventory_id
    inventory.save()
    return make_response(jsonify(inventory.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A INVENTORY
######################################################################
@app.route('/inventories/<int:inventory_id>', methods=['DELETE'])
def delete_inventories(inventory_id):
    """
    Delete a Inventory

    This endpoint will delete a Inventory based the id specified in the path
    """
    inventory = Inventory.find(inventory_id)
    if inventory:
        inventory.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)


######################################################################
# QUERY INVENTORIES
######################################################################


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def initialize_logging(log_level):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print 'Setting up logging...'
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.info('Logging handler established')


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    print "Inventory Service Starting..."
    initialize_logging(logging.INFO)
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
