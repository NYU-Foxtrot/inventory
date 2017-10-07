# Test cases can be run with:
# nosetests
# coverage report -m

""" Test cases for ProductInventory Model """

import unittest
from models import ProductInventory, ProductStatus, DataValidationError

######################################################################
#  T E S T   C A S E S
######################################################################
class TestProductInventorys(unittest.TestCase):
    """ Test Cases for ProductInventorys """

    def setUp(self):
        ProductInventory.remove_all()

    def test_create_ProductInventory(self):
        """ Create ProductInventory and assert that it exists """
        testInventory = ProductInventory(0, "shampoo", 1, ProductStatus.new)
        self.assertTrue(testInventory != None)
        self.assertEqual(testInventory.id, 0)
        self.assertEqual(testInventory.name, "shampoo")
        self.assertEqual(testInventory.status, ProductStatus.new)

    def test_add_ProductInventory(self):
        """ Create ProductInventory and add it to the database """
        products = ProductInventory.all()
        self.assertEqual(products, [])
        testInventory = ProductInventory(0, "shampoo", 2, ProductStatus.new)
        self.assertTrue(products!= None)
        self.assertEqual(testInventory.id, 0)
        testInventory.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(testInventory.id, 1)
        products = ProductInventory.all()
        self.assertEqual(len(products), 1)

    def test_update_ProductInventory(self):
        """ Update ProductInventory """
        testInventory = ProductInventory(0, "shampoo", 2, ProductStatus.new)
        testInventory.save()
        self.assertEqual(testInventory.id, 1)
        # Change it an save it, now it should be 10
        testInventory.quantity = 10
        testInventory.save()  
        self.assertEqual(testInventory.quantity, 10)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = ProductInventory.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].quantity, 10)

    def test_delete_ProductInventory(self):
        """ Delete ProductInventory """
        testInventory = ProductInventory(0, "shampoo", 1, ProductStatus.new)
        testInventory.save()
        self.assertEqual(len(ProductInventory.all()), 1)
        # delete the inventory specifying the id, name, quantity and status
        testInventory.delete()
        self.assertEqual(len(ProductInventory.all()), 0)

    def test_serialize_ProductInventory(self):
        """ Test serialization of ProductInventory """
        testInventory = ProductInventory(0, "shampoo", 1, ProductStatus.new)
        data =  testInventory.serialize() 
        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], 0)
        self.assertIn('name', data)
        self.assertEqual(data['name'], "shampoo")
        self.assertIn('status', data)
        self.assertEqual(data['status'], ProductStatus.new)

    def test_deserialize_ProductInventory(self):
        """ Test deserialization of ProductInventory """
        data = {"id": 1, "name": "shampoo", "quantity": 5, "status": ProductStatus.new}
        testInventory = ProductInventory()
        testInventory.deserialize(data)
        self.assertNotEqual(testInventory, None)
        self.assertEqual(testInventory.id, 1)
        self.assertEqual(testInventory.name, "shampoo")
        self.assertEqual(testInventory.status, ProductStatus.new)

    def test_deserialize_with_no_name(self):
        """ Deserialize ProductInventory without a name """
        testInventory = ProductInventory()
        data = {"id":0, "category": "cat"}
        self.assertRaises(DataValidationError, testInventory.deserialize, data)

    def test_deserialize_with_no_data(self):
        """ Deserialize ProductInventory with no data """
        testInventory = ProductInventory()
        self.assertRaises(DataValidationError, testInventory.deserialize, None)

    def test_deserialize_with_bad_data(self):
        """ Deserailize ProductInventory with bad data """
        testInventory = ProductInventory()
        self.assertRaises(DataValidationError, testInventory .deserialize, "data")

    def test_findProductInventory(self):
        """ Find ProductInventory by ID """   
        ProductInventory(0, "shampoo", 1, ProductStatus.new).save()
        ProductInventory(0, "soap", 1, ProductStatus.new).save()
        productInventory = ProductInventory.find(2)
        self.assertIsNot(productInventory, None)
        self.assertEqual(productInventory.id, 2)
        self.assertEqual(productInventory.name, "soap")

    def test_find_with_no_ProductInventorys(self):
        """ Find ProductInventory with no ProductInventorys """
        productInventory = ProductInventory.find(1)
        self.assertIs(productInventory, None)

    def test_ProductInventory_not_found(self):
        """ Test for ProductInventory that doesn't exist """
        ProductInventory(0, "shampoo", 1, ProductStatus.new).save()
        productInventory = ProductInventory.find(5)
        self.assertIs(productInventory, None)

    def test_find_by_status(self):
        """ Find ProductInventorys by status """
        ProductInventory(0, "shampoo", 1, ProductStatus.new).save()
        ProductInventory(0, "soap", 1, ProductStatus.new).save()
        productInventorys = ProductInventory.find_by_status(ProductStatus.new)
        self.assertEqual(len(productInventorys), 2)
  
    def test_find_by_name(self):
        """ Find ProductInventory by Name """
        ProductInventory(0, "shampoo", 1, ProductStatus.new).save()
        productInventorys = ProductInventory.find_by_name("shampoo")
        self.assertEqual(len(productInventorys), 1)
        self.assertEqual(productInventorys[0].name, "shampoo")


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestProductInventorys)
    # unittest.TextTestRunner(verbosity=2).run(suite)

   