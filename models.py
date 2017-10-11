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
import threading
#import enum


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


# class ProductStatus(enum.Enum):
#     new = 'new'
#     openBox = 'openBox'
#     used = 'used'


class Inventory(object):
    """
    Class that represents 

    This version uses an in-memory collection of Inventories for testing
    """
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
        """
        Saves inventory (in - memory data), replace the old inventory record if it already exists
        """
        if self.id == 0:
            self.id = self.__next_index()
            Inventory.data.append(self)
        else:
            for i in range(len(Inventory.data)):
                if Inventory.data[i].id == self.id:
                    Inventory.data[i] = self
                    break

    def delete(self):
        """ Delete inventory record with specified id, name, quantiy and status"""
        Inventory.data.remove(self)

    def serialize(self):
        """ Serializes Inventory into a dictionary """
        return {"id": self.id, "name": self.name, "quantity": self.quantity, "status": self.status}

    def deserialize(self, data):
        """
        Deserializes a Inventory from a dictionary

        Args:
            data (dict): A dictionary containing the Inventory data
        """
        if not isinstance(data, dict):
            raise DataValidationError('Invalid Inventory: body of request contained bad or no data')
        if data.has_key('id'):
            self.id = data['id']
        try:
            self.name = data['name']
            self.quantity = data['quantity']
            self.status = data['status']
        except KeyError as err:
            raise DataValidationError('Invalid Inventory: missing ' + err.args[0])
        return

    @staticmethod
    def __next_index():
        """ Generates the next index in a continual sequence """
        with Inventory.lock:
            Inventory.index += 1
        return Inventory.index

    @staticmethod
    def all():
        """ Returns all of the Inventories in the database """
        return [inventory for inventory in Inventory.data]

    @staticmethod
    def remove_all():
        """ Removes all of the Inventories from the database """
        del Inventory.data[:]
        Inventory.index = 0
        return Inventory.data

    @staticmethod
    def find(ProductInventory_id):
        """ Finds a Inventory by it's ID """
        if not Inventory.data:
            return None
        Inventories = [inventory for inventory in Inventory.data if
                             inventory.id == ProductInventory_id]
        if Inventories:
            return Inventories[0]
        return None

    @staticmethod
    def find_by_status(status):
        """ Returns all of the Inventories in a status

        Args:
         status (string): the status of the Inventories you want to match
        """
        return [inventory for inventory in Inventory.data if inventory.status == status]

    @staticmethod
    def find_by_quantity(quantity):
        """ Returns all of the Inventories in a status

        Args:
         quantity (int): the quantity of the Inventories you want to match
        """
        return [inventory for inventory in Inventory.data if inventory.quantity == quantity]

    @staticmethod
    def find_by_name(name):
        """ Returns all Inventories with the given name

        Args:
            name (string): the name of the Inventories you want to match
        """
        return [inventory for inventory in Inventory.data if inventory.name == name]
