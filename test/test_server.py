# Test cases can be run with:
# nosetests
# coverage report -m

""" Test cases for the Inventory Service """

import json
import logging
import unittest

from flask_api import status  # HTTP Status Codes
from mock import patch

from app import server


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
        server.Inventory(0, "shampoo", 2, 'new').save()
        server.Inventory(0, "conditioner", 5, 'new').save()
        self.app = server.app.test_client()

    def tearDown(self):
        """ Runs after each test """
        server.Inventory.remove_all()

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('Inventory Demo REST API Service', resp.data)
        # resp = self.app.get('/')
        # self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # data = json.loads(resp.data)
        # self.assertEqual(data['name'], 'Inventory Demo REST API Service')

    def test_get_inventory_list(self):
        """ Get a list of Inventories """
        resp = self.app.get('/inventories')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_get_inventory(self):
        """ Get one Inventory """
        resp = self.app.get('/inventories/2')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'conditioner')

    def test_get_inventory_not_found(self):
        """ Get a Inventory that's not found """
        resp = self.app.get('/inventories/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_inventory(self):
        """ Create a Inventory """
        # save the current number of inventories for later comparrison
        inventory_count = self.get_inventory_count()
        # add a new inventory
        new_inventory = {'name': 'body wash', 'quantity': 1, 'status': 'new'}
        data = json.dumps(new_inventory)
        resp = self.app.post('/inventories', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['name'], 'body wash')
        # check that count has gone up and includes body wash
        resp = self.app.get('/inventories')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), inventory_count + 1)
        self.assertIn(new_json, data)

    def test_create_inventory_with_no_name(self):
        """ Create a Inventory with the name missing """
        new_inventory = {'status': 'new'}
        data = json.dumps(new_inventory)
        resp = self.app.post('/inventories', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

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

    def test_query_inventory_quantity(self):
        """ Get a list of Inventories with quantity """
        resp = self.app.get('/inventories', query_string='quantity=5')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertTrue('conditioner' in resp.data)
        self.assertFalse('shampoo' in resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['quantity'], 5)

    def test_query_inventory_found(self):
        """ Query Inventories by Status found target"""
        resp = self.app.get('/inventories/query', query_string='name=shampoo&status=new')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('shampoo' in resp.data)
        self.assertFalse('conditioner' in resp.data)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 1)

    def test_query_inventory_not_found(self):
        """ Query Inventories by field not found target"""
        resp = self.app.get('/inventories/query', query_string='name=shampoo&status=used')
        self.assertEquals(resp.status_code, 404)

    def test_count_inventories_quantity(self):
        """ Count total quantity of product"""
        # add a new inventory
        new_inventory = {'name': 'body wash', 'quantity': 2, 'status': 'new'}
        used_inventory2 = {'name': 'body wash', 'quantity': 1, 'status': 'used'}
        data = json.dumps(new_inventory)
        data2 = json.dumps(used_inventory2)

        resp = self.app.post('/inventories', data=data, content_type='application/json')
        resp2 = self.app.post('/inventories', data=data2, content_type='application/json')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)

        resp = self.app.get('/inventories/count', query_string='name=body wash')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['count'], 3)

    def test_method_not_allowed(self):
        """ Call a Method thats not Allowed """
        resp = self.app.post('/inventories/0')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch('app.models.Inventory.find_by_name')
    def test_mock_search_data_internal_error(self, Inventory_find_mock):
        """ Mocking the 500 ERROR """
        Inventory_find_mock.side_effect = OSError()
        #query_info = {'name': 'shampoo', 'status':'new'}
        resp = self.app.get('/inventories/query', query_string='name=shampoo&status=new',content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_415_unsupported_media_type(self):
        """ Update an Inventory """
        new_shampoo = {'name': 'shampoo', 'quantity': 8, 'status': 'new'}
        data = json.dumps(new_shampoo)
        resp = self.app.put('/inventories/1', data=data, content_type='string')
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


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
