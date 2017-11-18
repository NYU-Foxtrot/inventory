# Copyright 2017 NYU-FOXTROT. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Models for Inventory in inventory

All of the models are stored in this module

Models
------
Inventory - Inventory used in inventory management and operation

Attributes:
-----------
id (int) - uuid used to identify one inventory record 
name (string) - the name of the product
quantity(int) - amount of Product Inventories
status (string) - the status of the inventory : new, openBox and used

"""

"""
Inventory Model that uses Redis

You must initlaize this class before use by calling inititlize().
This class looks for an environment variable called VCAP_SERVICES
to get it's database credentials from. If it cannot find one, it
tries to connect to Redis on the localhost. If that fails it looks
for a server name 'redis' to connect to.
"""

import threading
# import enum
import os
import json
import logging
import pickle
from cerberus import Validator
from redis import Redis
from redis.exceptions import ConnectionError


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

######################################################################
# Inventory Model for database
#   This class must be initialized with use_db(redis) before using
#   where redis is a value connection to a Redis database
######################################################################

class Inventory(object):
    """ Inventory interface to database """

    logger = logging.getLogger(__name__)
    redis = None
    schema = {
        'id': {'type': 'integer'},
        'name': {'type': 'string', 'required': True},
        'quantity': {'type': 'integer', 'required': True},
        'status': {'type': 'string', 'required': True}
    }
    __validator = Validator(schema)

    lock = threading.Lock()
    data = []
    index = 0

    def __init__(self, inventoryid=0, name='', quantity=0, status=''):
        """ Initialize a Inventory """
        self.id = inventoryid
        self.name = name
        self.quantity = quantity
        self.status = status

    def save(self):
        """ Saves an Inventory in the database """
        if self.name is None:  # name is the only required field
            raise DataValidationError('name attribute is not set')
        if self.id == 0:
            self.id = Inventory.__next_index()
        Inventory.redis.set(self.id, pickle.dumps(self.serialize()))
        # """
        # Saves inventory (in - memory data), replace the old inventory record if it already exists
        # """
        # if self.id == 0:
        #     self.id = self.__next_index()
        #     Inventory.data.append(self)
        # else:
        #     for i in range(len(Inventory.data)):
        #         if Inventory.data[i].id == self.id:
        #             Inventory.data[i] = self
        #             break

    def delete(self):
        """ Deletes an Inventory from the database """
        Inventory.redis.delete(self.id)
        # """ Delete inventory record with specified id, name, quantiy and status"""
        # Inventory.data.remove(self)

    def serialize(self):
        """ Serializes an Inventory into a dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "status": self.status
        }
        # """ Serializes Inventory into a dictionary """
        # return {"id": self.id, "name": self.name, "quantity": self.quantity, "status": self.status}

    def deserialize(self, data):
        """ Deserializes an Inventory, marshalling the data """
        if isinstance(data, dict) and Inventory.__validator.validate(data):
            self.name = data['name']
            self.quantity = data['quantity']
            self.status = data['status']
        else:
            raise DataValidationError('Invalid Inventory data: ' + str(Inventory.__validator.errors))
        return self
        # """
        # Deserializes a Inventory from a dictionary
        #
        # Args:
        #     data (dict): A dictionary containing the Inventory data
        # """
        # if not isinstance(data, dict):
        #     raise DataValidationError('Invalid Inventory: body of request contained bad or no data')
        # if data.has_key('id'):
        #     self.id = data['id']
        # try:
        #     self.name = data['name']
        #     self.quantity = data['quantity']
        #     self.status = data['status']
        # except KeyError as err:
        #     raise DataValidationError('Invalid Inventory: missing ' + err.args[0])
        # return

    ######################################################################
    #  S T A T I C   D A T A B S E   M E T H O D S
    ######################################################################

    @staticmethod
    def __next_index():
        """ Increments the index and returns it """
        return Inventory.redis.incr('index')
        # """ Generates the next index in a continual sequence """
        # with Inventory.lock:
        #     Inventory.index += 1
        # return Inventory.index

    @staticmethod
    def use_db(redis):
        Inventory.__redis = redis

    @staticmethod
    def all():
        """ Query that returns all Inventories """
        results = []
        for key in Inventory.redis.keys():
            if key != 'index':  # filer out our id index
                data = pickle.loads(Inventory.redis.get(key))
                inventory = Inventory(data['id']).deserialize(data)
                results.append(inventory)
        return results
        # """ Returns all of the Inventories in the database """
        # return [inventory for inventory in Inventory.data]

    @staticmethod
    def remove_all():
        """ Removes all Inventories from the database """
        Inventory.redis.flushall()
        # """ Removes all of the Inventories from the database """
        # del Inventory.data[:]
        # Inventory.index = 0
        # return Inventory.data

    ######################################################################
    #  F I N D E R   M E T H O D S
    ######################################################################

    @staticmethod
    def find(inventory_id):
        """ Query that finds Inventories by their id """
        if Inventory.redis.exists(inventory_id):
            data = pickle.loads(Inventory.redis.get(inventory_id))
            inventory = Inventory(data['id']).deserialize(data)
            return inventory
        return None
        # """ Finds a Inventory by it's ID """
        # if not Inventory.data:
        #     return None
        # Inventories = [inventory for inventory in Inventory.data if
        #                      inventory.id == ProductInventory_id]
        # if Inventories:
        #     return Inventories[0]
        # return None

    @staticmethod
    def __find_by(attribute, value):
        """ Generic Query that finds a key with a specific value """
        # return [inventory for inventory in Inventory.__data if inventory.category == category]
        Inventory.logger.info('Processing %s query for %s', attribute, value)
        if isinstance(value, str):
            search_criteria = value.lower()  # make case insensitive
        else:
            search_criteria = value
        results = []
        for key in Inventory.redis.keys():
            if key != 'index':  # filer out our id index
                data = pickle.loads(Inventory.redis.get(key))
                # perform case insensitive search on strings
                if isinstance(data[attribute], str):
                    test_value = data[attribute].lower()
                else:
                    test_value = data[attribute]
                if test_value == search_criteria:
                    results.append(Inventory(data['id']).deserialize(data))
        return results

    @staticmethod
    def find_by_status(status):
        """ Query that finds Inventories by their status """
        return Inventory.__find_by('status', status)
        # """ Returns all of the Inventories in a status
        #
        # Args:
        #  status (string): the status of the Inventories you want to match
        # """
        # return [inventory for inventory in Inventory.data if inventory.status == status]

    @staticmethod
    def find_by_quantity(quantity):
        """ Query that finds Inventories by their quantity """
        return Inventory.__find_by('quantity', quantity)
        # """ Returns all of the Inventories in a status
        #
        # Args:
        #  quantity (int): the quantity of the Inventories you want to match
        # """
        # return [inventory for inventory in Inventory.data if inventory.quantity == quantity]

    @staticmethod
    def find_by_name(name):
        """ Query that finds Inventories by their name """
        return Inventory.__find_by('name', name)
        # """ Returns all Inventories with the given name
        #
        # Args:
        #     name (string): the name of the Inventories you want to match
        # """
        # return [inventory for inventory in Inventory.data if inventory.name == name]

    ######################################################################
    #  R E D I S   D A T A B A S E   C O N N E C T I O N   M E T H O D S
    ######################################################################

    @staticmethod
    def connect_to_redis(hostname, port, password):
        """ Connects to Redis and tests the connection """
        Inventory.logger.info("Testing Connection to: %s:%s", hostname, port)
        Inventory.redis = Redis(host=hostname, port=port, password=password)
        try:
            Inventory.redis.ping()
            Inventory.logger.info("Connection established")
        except ConnectionError:
            Inventory.logger.info("Connection Error from: %s:%s", hostname, port)
            Inventory.redis = None
        return Inventory.redis

    @staticmethod
    def init_db(redis=None):
        """
        Initialized Redis database connection
        This method will work in the following conditions:
          1) In Bluemix with Redis bound through VCAP_SERVICES
          2) With Redis running on the local server as with Travis CI
          3) With Redis --link in a Docker container called 'redis'
          4) Passing in your own Redis connection object
        Exception:
        ----------
          redis.ConnectionError - if ping() test fails
        """
        if redis:
            Inventory.logger.info("Using client connection...")
            Inventory.redis = redis
            try:
                Inventory.redis.ping()
                Inventory.logger.info("Connection established")
            except ConnectionError:
                Inventory.logger.error("Client Connection Error!")
                Inventory.redis = None
                raise ConnectionError('Could not connect to the Redis Service')
            return
        # Get the credentials from the Bluemix environment
        if 'VCAP_SERVICES' in os.environ:
            Inventory.logger.info("Using VCAP_SERVICES...")
            vcap_services = os.environ['VCAP_SERVICES']
            services = json.loads(vcap_services)
            creds = services['rediscloud'][0]['credentials']
            Inventory.logger.info("Conecting to Redis on host %s port %s",
                                  creds['hostname'], creds['port'])
            Inventory.connect_to_redis(creds['hostname'], creds['port'], creds['password'])
        else:
            Inventory.logger.info("VCAP_SERVICES not found, checking localhost for Redis")
            Inventory.connect_to_redis('127.0.0.1', 6379, None)
            if not Inventory.redis:
                Inventory.logger.info("No Redis on localhost, looking for redis host")
                Inventory.connect_to_redis('redis', 6379, None)
        if not Inventory.redis:
            # if you end up here, redis instance is down.
            Inventory.logger.fatal('*** FATAL ERROR: Could not connect to the Redis Service')
            raise ConnectionError('Could not connect to the Redis Service')
