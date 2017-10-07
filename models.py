# Copyright 2016, 2017 John Rofrano. All Rights Reserved.
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
Models for ProductInventory in inventory

All of the models are stored in this module

Models
------
ProductInventory - ProductInventory used in inventory management and operation

Attributes:
-----------
id (int) - uuid used to identify one inventory record 
name (string) - the name of the product
quantity(int) - amount of Product Inventorys
status (string) - the status of the inventory : new, openBox and used

"""
import threading
import enum

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

class ProductStatus(enum.Enum):
    new = 'new'
    damaged = 'openBox'
    used = 'used'
 
class ProductInventory(object):
    """
    Class that represents 

    This version uses an in-memory collection of ProductInventorys for testing
    """
    lock = threading.Lock()
    data = []
    index = 0

    def __init__(self, id=0, name='', quantity=0, status=ProductStatus.new):
        """ Initialize a ProductInventory """
        self.id = id
        self.name = name
        self.quantity = quantity
        self.status = status

    def save(self):
        """
        Saves inventory (in - memory data), replace the old inventory record if it already exists
        """
        if self.id == 0:
            self.id = self.__next_index() 
            ProductInventory.data.append(self)
        else:
            for i in range(len(ProductInventory.data)):
                if ProductInventory.data[i].id == self.id:
                    ProductInventory.data[i] = self
                    break

    def delete(self):
        """ Delete inventory record with specified id, name, quantiy and status"""
        ProductInventory.data.remove(self)

    def serialize(self):
        """ Serializes ProductInventory into a dictionary """
        return {"id": self.id, "name": self.name, "status": self.status}

    def deserialize(self, data):
        """
        Deserializes a ProductInventory from a dictionary

        Args:
            data (dict): A dictionary containing the ProductInventory data
        """
        if not isinstance(data, dict):
            raise DataValidationError('Invalid ProductInventory: body of request contained bad or no data')
        if data.has_key('id'):
            self.id = data['id']
        try:
            self.name = data['name']
            self.status = data[ 'status']
        except KeyError as err:
            raise DataValidationError('Invalid ProductInventory: missing ' + err.args[0])
        return

    @staticmethod
    def __next_index():
        """ Generates the next index in a continual sequence """
        with ProductInventory.lock:
            ProductInventory.index += 1
        return ProductInventory.index

    @staticmethod
    def all():
        """ Returns all of the ProductInventorys in the database """
        return [productInventory for productInventory in ProductInventory.data]

    @staticmethod
    def remove_all():
        """ Removes all of the ProductInventorys from the database """
        del ProductInventory.data[:]
        ProductInventory.index = 0
        return ProductInventory.data

    @staticmethod
    def find(ProductInventory_id):
        """ Finds a ProductInventory by it's ID """
        if not ProductInventory.data:
            return None
        ProductInventorys = [productInventory for productInventory in ProductInventory.data if productInventory.id == ProductInventory_id]
        if ProductInventorys:
            return ProductInventorys[0]
        return None

    @staticmethod
    def find_by_status(status):
        """ Returns all of the ProductInventorys in a status

        Args:
         status (string): the status of the ProductInventorys you want to match
        """
        return [productInventory for productInventory in ProductInventory.data if productInventory.status == status]

    @staticmethod
    def find_by_name(name):
        """ Returns all ProductInventorys with the given name

        Args:
            name (string): the name of the ProductInventorys you want to match
        """
        return [productInventory for productInventory in ProductInventory.data if productInventory.name == name]
