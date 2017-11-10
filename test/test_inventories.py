# Test cases can be run with:
# nosetests
# coverage report -m

""" Test cases for Inventory Model """

import unittest

from app.models import Inventory, DataValidationError

VCAP_SERVICES = {
    'rediscloud': [
        {'credentials': {
            'password': '',
            'hostname': '127.0.0.1',
            'port': '6379'
        }
        }
    ]
}


######################################################################
#  T E S T   C A S E S
######################################################################
class Testinventories(unittest.TestCase):
    """ Test Cases for inventories """

    def setUp(self):
        """ Initialize the Redis database """
        Inventory.init_db()
        Inventory.remove_all()

    def test_create_Inventory(self):
        """ Create Inventory and assert that it exists """
        testInventory = Inventory(0, "shampoo", 1, "new")
        self.assertTrue(testInventory != None)
        self.assertEqual(testInventory.id, 0)
        self.assertEqual(testInventory.name, "shampoo")
        self.assertEqual(testInventory.status, "new")

    def test_add_Inventory(self):
        """ Create Inventory and add it to the database """
        products = Inventory.all()
        self.assertEqual(products, [])
        testInventory = Inventory(0, "shampoo", 2, "new")
        self.assertTrue(products != None)
        self.assertEqual(testInventory.id, 0)
        testInventory.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(testInventory.id, 1)
        products = Inventory.all()
        self.assertEqual(len(products), 1)

    def test_update_Inventory(self):
        """ Update Inventory """
        testInventory = Inventory(0, "shampoo", 2, "new")
        testInventory.save()
        self.assertEqual(testInventory.id, 1)
        # Change it an save it, now it should be 10
        testInventory.quantity = 10
        testInventory.save()
        self.assertEqual(testInventory.quantity, 10)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = Inventory.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].quantity, 10)

    def test_delete_Inventory(self):
        """ Delete Inventory """
        testInventory = Inventory(0, "shampoo", 1, "new")
        testInventory.save()
        self.assertEqual(len(Inventory.all()), 1)
        # delete the inventory specifying the id, name, quantity and status
        testInventory.delete()
        self.assertEqual(len(Inventory.all()), 0)

    def test_serialize_Inventory(self):
        """ Test serialization of Inventory """
        testInventory = Inventory(0, "shampoo", 2, "new")
        data = testInventory.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], 0)
        self.assertIn('name', data)
        self.assertEqual(data['name'], "shampoo")
        self.assertIn('quantity', data)
        self.assertEqual(data['quantity'], 2)
        self.assertIn('status', data)
        self.assertEqual(data['status'], "new")

    def test_deserialize_Inventory(self):
        """ Test deserialization of Inventory """
        data = {"id": 1, "name": "shampoo", "quantity": 2, "status": "new"}
        testInventory = Inventory(data['id'])
        testInventory.deserialize(data)
        self.assertNotEqual(testInventory, None)
        self.assertEqual(testInventory.id, 1)
        self.assertEqual(testInventory.name, "shampoo")
        self.assertEqual(testInventory.quantity, 2)
        self.assertEqual(testInventory.status, "new")

    def test_deserialize_with_no_name(self):
        """ Deserialize Inventory without a name """
        testInventory = Inventory()
        data = {"id": 0, "quantity": 2, "status": "new"}
        self.assertRaises(DataValidationError, testInventory.deserialize, data)

    def test_deserialize_with_no_data(self):
        """ Deserialize Inventory with no data """
        testInventory = Inventory()
        self.assertRaises(DataValidationError, testInventory.deserialize, None)

    def test_deserialize_with_bad_data(self):
        """ Deserailize Inventory with bad data """
        testInventory = Inventory()
        self.assertRaises(DataValidationError, testInventory.deserialize, "data")

    def test_findInventory(self):
        """ Find Inventory by ID """
        Inventory(0, "shampoo", 1, "new").save()
        Inventory(0, "soap", 1, "new").save()
        inventory = Inventory.find(2)
        self.assertIsNot(inventory, None)
        self.assertEqual(inventory.id, 2)
        self.assertEqual(inventory.name, "soap")

    def test_find_with_no_inventories(self):
        """ Find Inventory with no inventories """
        inventory = Inventory.find(1)
        self.assertIs(inventory, None)

    def test_Inventory_not_found(self):
        """ Test for Inventory that doesn't exist """
        Inventory(0, "shampoo", 1, "new").save()
        inventory = Inventory.find(5)
        self.assertIs(inventory, None)

    def test_find_by_status(self):
        """ Find Inventory by Status """
        Inventory(0, "shampoo", 1, "new").save()
        Inventory(0, "soap", 1, "new").save()
        inventories = Inventory.find_by_status("new")
        inventories2 = Inventory.find_by_status("used")

        self.assertEqual(len(inventories), 2)
        self.assertEqual(len(inventories2), 0)

    def test_find_by_quantity(self):
        """ Find Inventory by Quantity """
        Inventory(0, "shampoo", 1, "new").save()
        inventories = Inventory.find_by_quantity(1)
        self.assertEqual(len(inventories), 1)
        self.assertEqual(inventories[0].quantity, 1)

    def test_find_by_name(self):
        """ Find Inventory by Name """
        Inventory(0, "shampoo", 1, "new").save()
        inventories = Inventory.find_by_name("shampoo")
        self.assertEqual(len(inventories), 1)
        self.assertEqual(inventories[0].name, "shampoo")


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(Testinventories)
    # unittest.TextTestRunner(verbosity=2).run(suite)
