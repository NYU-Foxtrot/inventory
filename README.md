# inventory
This is the inventory application using [Flask microframework](http://flask.pocoo.org/) for NYU course *NYU DevOps Spring 2017 * [CSCI-GA.3033-013](http://cs.nyu.edu/courses/spring17/CSCI-GA.3033-013/)

## Prerequisite Installation using Vagrant
The app requires Vagrant and VirtualBox. if you don't have this software the first step is down download and install [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/)

## Setup
From a terminal navigate to a location where this application code is and issue:
```bash
    $ vagrant up
    $ vagrant ssh
    $ cd /vagrant
```
This will place you into an Ubuntu VM all set to run the code.

## Calls available

    * list_inventories() -- This code is called on the URL GET /inventories, used to return all of the Inventories. No input needed.
    * get_inventories(inventory_id): -- This code is called on the URL GET /inventories/<int:inventory_id>, used to retrieve a single Inventory. Input should be the inventory id to be retrieved.
    * create_inventories(): -- This code is called on the URL POST /inventories, used to create a new inventory. No input needed.
    * update_inventories(inventory_id): -- This code is called on the URL PUT /inventories/<int:inventory_id>, used to update a Inventory. Input should be the inventory id to be updated.
    * delete_inventories(inventory_id): -- This code is called on the URL DELETE /inventories/<int:inventory_id>, used to delete a Inventory. Input should be the inventory id to be deleted.
    * count_inventories_quantity(): -- This code is called on the URL GET /inventories/count, used to return a list of inventory. No input needed.
    * query_inventories_by_name_status(): -- This code is called on the URL GET /inventories/query, used to query inventories by name and status. No input needed.
    
## Tests

Run Code Coverage to see how well your test cases exercise your code:

    $ coverage run test_server.py
    $ coverage report -m --include=server.py

This is particularly useful because it reports the line numbers for the code that is not covered so that you can write more test cases.

You can even run `nosetests` with `coverage`

    $ nosetests --with-coverage --cover-package=server

Try and get as close to 100% coverage as you can.

Run the tests using `nose` and make sure that everything works as expected.

    $ nosetests
    $ coverage report -m

Nose is configured to automatically include the flags `--with-spec --spec-color` so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

You can run the code to test it out in your browser with the following command:

    $ python server.py

You should be able to see it at: http://localhost:5000/

When you are done, you can exit and shut down the vm with:

    $ exit
    $ vagrant halt

If the VM is no longer needed you can remove it with:

    $ vagrant destroy
    
## What's featured in the project?

    * server.py -- the main Service using Python Flask
    * test_server.py -- test cases using unittest
    * test_inventories.py -- test cases using just the Inventory model
    * models.py -- hold your model definitions of resource
