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
GET / - Displays a UI for Selenium testing
GET /inventories - returns a list all of the Inventories
GET /inventories/{id} - returns the Inventory with a given id number
POST /inventories - creates a new Inventory record in the database
PUT /inventories/{id} - updates a Inventory record in the database
DELETE /inventories/{id} - deletes a Inventory record in the database
GET /inventories/count - returns total amount of product with given name/id/status(whatever status)
GET /inventories/query - returns the inventory record based on the query string (name and status)
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, json, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes
from flask_restplus import Api as BaseApi, Resource, fields
from werkzeug.exceptions import NotFound
from app.models import Inventory, DataValidationError, DatabaseConnectionError
from . import app

# https://github.com/noirbizarre/flask-restplus/issues/247
class Api(BaseApi):

    def _register_doc(self, app_or_blueprint):
        # HINT: This is just a copy of the original implementation with the last line commented out.
        if self._add_specs and self._doc:
            # Register documentation before root if enabled
            app_or_blueprint.add_url_rule(self._doc, 'doc', self.render_doc)
        #app_or_blueprint.add_url_rule(self._doc, 'root', self.render_root)

    @property
    def base_path(self):
        return ''

######################################################################
# Configure Swagger before initilaizing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Inventory REST API Service',
          description='This is an Inventory server.',
          doc='/swagger/'
         )

# This namespace is the start of the path i.e., /inventories
ns = api.namespace('inventories', description='Inventory operations')

# Define the model so that the docs reflect what can be sent
inventory_model = api.model('Inventory', {
    'id': fields.Integer(readOnly=True,
                         description='The unique id assigned internally by service'),
    'name': fields.String(required=True,
                          description='The name of the Inventory'),
    'quantity': fields.Integer(required=True,
                              description='The amount of Inventory'),
    'status': fields.String(required=True,
                                description='Status of the Inventory (e.g. new, used, openBox)')

})


# Error handlers reuire app to be initialized so we must import
# then only after we have initialized the Flask app instance

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = error.message or str(error)
    app.logger.info(message)
    return {'status':400, 'error': 'Bad Request', 'message': message}, 400

@api.errorhandler(DatabaseConnectionError)
def database_connection_error(error):
    """ Handles Database Errors from connection attempts """
    message = error.message or str(error)
    app.logger.critical(message)
    return {'status':500, 'error': 'Server Error', 'message': message}, 500

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
# GET HEALTH CHECK
######################################################################
@app.route('/healthcheck')
def healthcheck():
    """ Let them know our heart is still beating """
    return make_response(jsonify(status=200, message='Healthy'), status.HTTP_200_OK)

######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Root URL response """
    app.logger.info("here in method")
    return app.send_static_file('index.html')
    # return jsonify(name='Inventory Demo REST API Service',
    #                version='1.0',
    #                paths=url_for('list_inventories', _external=True)
    #                ), status.HTTP_200_OK


######################################################################
#  PATH: /inventories/{id}
######################################################################
@ns.route('/<int:inventory_id>')
@ns.param('inventory_id', 'The Inventory identifier')
class InventoryResource(Resource):
    """
    InventoryResource class
    Allows the manipulation of a single Inventory
    GET /inventory{id} - Returns an Inventory with the id
    PUT /inventory{id} - Update an Inventory with the id
    DELETE /inventory{id} -  Deletes an Inventory with the id
    """

    #------------------------------------------------------------------
    # RETRIEVE AN INVENTORY
    #------------------------------------------------------------------
    @ns.doc('get_inventories')
    @ns.response(404, 'Inventory not found')
    @ns.marshal_with(inventory_model)
    def get(self, inventory_id):
        """
        Retrieve a single Inventory
        This endpoint will return a Inventory based on it's id
        """
        app.logger.info("Request to Retrieve an inventory with id [%s]", inventory_id)
        inventory = Inventory.find(inventory_id)
        if not inventory:
            raise NotFound("Inventory with id '{}' was not found.".format(inventory_id))
        return inventory.serialize(), status.HTTP_200_OK

    #------------------------------------------------------------------
    # UPDATE AN EXISTING INVENTORY
    #------------------------------------------------------------------
    @ns.doc('update_inventories')
    @ns.response(404, 'Inventory not found')
    @ns.response(400, 'The posted Inventory data was not valid')
    @ns.expect(inventory_model)
    @ns.marshal_with(inventory_model)
    def put(self, inventory_id):
        """
        Update an Inventory
        This endpoint will update an Inventory based the body that is posted
        """
        app.logger.info('Request to Update a inventory with id [%s]', inventory_id)
        check_content_type('application/json')
        inventory = Inventory.find(inventory_id)
        if not inventory:
            #api.abort(404, "Inventory with id '{}' was not found.".format(inventory_id))
            raise NotFound('Inventory with id [{}] was not found.'.format(inventory_id))
        #data = request.get_json()
        data = api.payload
        app.logger.info(data)
        inventory.deserialize(data)
        inventory.id = inventory_id
        inventory.save()
        return inventory.serialize(), status.HTTP_200_OK

    #------------------------------------------------------------------
    # DELETE AN INVENTORY
    #------------------------------------------------------------------
    @ns.doc('delete_inventories')
    @ns.response(204, 'Inventory deleted')
    def delete(self, inventory_id):
        """
        Delete an Inventory
        This endpoint will delete a Inventory based the id specified in the path
        """
        app.logger.info('Request to Delete a inventory with id [%s]', inventory_id)
        inventory = Inventory.find(inventory_id)
        if inventory:
            inventory.delete()
        return '', status.HTTP_204_NO_CONTENT



######################################################################
#  PATH: /inventories
######################################################################
@ns.route('/', strict_slashes=False)
class InventoryCollection(Resource):
    """ Handles all interactions with collections of Inventories """
    #------------------------------------------------------------------
    # LIST ALL INVENTORIES
    #------------------------------------------------------------------
    @ns.doc('list_inventories')
    @ns.param('quantity', 'List Inventories by quantity')
    @ns.param('status', 'List Inventories by status')
    @ns.param('name', 'List Inventories by name')
    @ns.marshal_list_with(inventory_model)
    def get(self):
        """
        Returns all of the Inventories
        This endpoint will return all inventories by given name, status and quantity
        """
        app.logger.info('Request to list Inventories...')
        inventories = []
        quantity = request.args.get('quantity')
        status = request.args.get('status')
        name = request.args.get('name')
        if quantity:
            q = int(quantity)
            inventories = Inventory.find_by_quantity(q)
        elif status:
            inventories = Inventory.find_by_status(status)
        elif name:
            inventories = Inventory.find_by_name(name)
        else:
            inventories = Inventory.all()
        

        app.logger.info('[%s] Inventories returned', len(inventories))
        results = [inventory.serialize() for inventory in inventories]
        return results

    #------------------------------------------------------------------
    # ADD A NEW INVENTORY
    #------------------------------------------------------------------
    @ns.doc('create_inventories')
    @ns.expect(inventory_model)
    @ns.response(400, 'The posted data was not valid')
    @ns.response(201, 'Inventory created successfully')
    @ns.marshal_with(inventory_model, code=201)
    def post(self):
        """
        Creates an Inventory
        This endpoint will create an Inventory based the data in the body that is posted
        """
        app.logger.info('Request to Create a Inventory')
        check_content_type('application/json')
        inventory = Inventory()
        app.logger.info('Payload = %s', api.payload)
        inventory.deserialize(api.payload)
        inventory.save()
        app.logger.info('Inventory with new id [%s] saved!', inventory.id)
        location_url = api.url_for(InventoryResource, inventory_id=inventory.id, _external=True)
        return inventory.serialize(), status.HTTP_201_CREATED, {'Location': location_url}


######################################################################
#  PATH: /inventories/count
######################################################################
@ns.route('/count')
@ns.param('name', 'Count inventories by name')
class PurchaseResource(Resource):
    """ Count actions on an Inventory """
    @ns.doc('count_inventories')
    @ns.response(404, 'Inventory not found')
    @ns.response(409, 'The Inventory is not available for count')
    def get(self):
        """
        Count an Inventory
        This endpoint will count inventory with given name
        """
        app.logger.info('Request to Count an Inventory')
        name = request.args.get('name')
        if name:
            results = Inventory.find_by_name(name)
            quantities = [record.quantity for record in results]
            quantity_sum = sum(quantities)
            inventories_by_name = Inventory.find_by_name(name)
            results1 = [inventory.serialize() for inventory in inventories_by_name]
        
        resp = {'records': results1, 'name':name, 'count': quantity_sum}    
        app.logger.info('Inventory with name [%s] has been counted!', inventory.name)
        return resp, status.HTTP_200_OK


######################################################################
#  PATH: /inventories/query
######################################################################
@ns.route('/query')
@ns.param('name', 'Query inventories by name')
@ns.param('status', 'Query inventories by status')
class QueryResource(Resource):
    """ Query actions on an Inventory """
    @ns.doc('query_inventories')
    @ns.response(404, 'Inventory not found')
    @ns.response(409, 'The Inventory is not available for query')
    def get(self):
        """
        Query an Inventory
        This endpoint will query inventory with given name and status
        """
        app.logger.info('Request to Query an Inventory')
        name = request.args.get('name')
        status = request.args.get('status')
        inventories_by_name = Inventory.find_by_name(name)
        inventories_by_status = Inventory.find_by_status(status)
        if not inventories_by_status or not inventories_by_name:
            raise NotFound("Query Inventory with name '{}' and status '{}'  was not found.".format(name, status))
        results1 = [inventory.serialize() for inventory in inventories_by_name]
        results2 = [inventory.serialize() for inventory in inventories_by_status]
        results = [r for r in results1 if r in results2]
            
        app.logger.info('[%s] Inventories returned', len(results))
        return results


######################################################################
# DELETE ALL INVENTORY DATA (for testing only)
######################################################################
@app.route('/inventories/reset', methods=['DELETE'])
def inventories_reset():
    """ Removes all inventories from the database """
    Inventory.remove_all()
    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
@app.before_first_request
def init_db(redis=None):
    """ Initlaize the model """
    Inventory.init_db(redis)


# load sample data
def data_load(payload):
    """ Loads an Inventory into the database """
    inventory = Inventory(0, payload['name'], payload['quantity'], payload['status'])
    inventory.save()


def data_reset():
    """ Removes all Inventories from the database """
    Inventory.remove_all()


def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] == content_type:
        return
    app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 'Content-Type must be {}'.format(content_type))


def initialize_logging(log_level=logging.INFO):
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
