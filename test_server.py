# Test cases can be run with:
# nosetests
# coverage report -m

""" Test cases for the Inventory Service """

import logging
import unittest
import json
from mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
import server


######################################################################
#  T E S T   C A S E S
######################################################################
class TestInventoryServer(unittest.TestCase):
    """ Inventory Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        server.app.debug = False
        server.initialize_logging(logging.ERROR)

    def setUp(self):
        """ Runs before each test """
        server.Inventory.remove_all()
        server.Inventory(0, "shampoo", 2, "new").save()
        server.Inventory(0, "conditioner", 5, "new").save()
        self.app = server.app.test_client()

    def tearDown(self):
        """ Runs after each test """
        server.Inventory.remove_all()

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'Inventory Demo REST API Service')

    def test_get_inventory_list(self):
        """ Get a list of Inventories """
        resp = self.app.get('/inventories')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_get_inventory(self):
        """ Get one Inventory """

    def test_get_inventory_not_found(self):
        """ Get a Inventory that's not found """

    def test_create_inventory(self):
        """ Create a Inventory """

    def test_create_inventory_with_no_name(self):
        """ Create a Inventory with the name missing """

    def test_update_inventory(self):
        """ Update an Inventory """
        new_shampoo = {'name': 'shampoo', 'quantity': 8, 'status': 'new'}
        data = json.dumps(new_shampoo)
        resp = self.app.put('/inventories/1', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.app.get('/inventories/1', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['quantity'], 8)

    def test_update_inventory_with_no_name(self):
        """ Update a Inventory with no name """
        new_inventory = {'id': 2, 'quantity': 2, 'status': 'new'}
        data = json.dumps(new_inventory)
        resp = self.app.put('/inventories/2', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_inventory_not_found(self):
        """ Update a Inventory that can't be found """
        new_inventory = {'name': 'conditioner', 'quantity': 1, 'status': 'new'}
        data = json.dumps(new_inventory)
        resp = self.app.put('/inventories/0', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_inventory(self):
        """ Delete a Inventory that exists """
        # save the current number of inventories for later comparision
        inventory_count = self.get_inventory_count()
        # delete a inventory
        resp = self.app.delete('/inventories/1', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        new_count = self.get_inventory_count()
        self.assertEqual(new_count, inventory_count - 1)

    def test_query_inventory_list_by_category(self):
        """ Query Inventories by Category """

    def test_query_inventory_list_by_name(self):
        """ Query Inventories by Name """

    ######################################################################
    # Utility functions
    ######################################################################

    def get_inventory_count(self):
        """ save the current number of inventories """
        resp = self.app.get('/inventories')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        return len(data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()