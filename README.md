# inventory

[![Build Status](https://travis-ci.org/NYU-Foxtrot/inventory.svg?branch=moveFileToAppFolder)](https://travis-ci.org/NYU-Foxtrot/inventory)

This is the inventory application using [Flask microframework](http://flask.pocoo.org/) for NYU course `NYU DevOps Spring 2017` [CSCI-GA.3033-013](http://cs.nyu.edu/courses/spring17/CSCI-GA.3033-013/)

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

    list_inventories() -- This code is called on the URL GET /inventories
Used to return all of the Inventories. No input needed.

    get_inventories(inventory_id): -- This code is called on the URL GET /inventories/<int:inventory_id>
Used to retrieve a single Inventory. Input should be the inventory id to be retrieved.

    create_inventories(): -- This code is called on the URL POST /inventories.
Used to create a new inventory. No input needed.

    update_inventories(inventory_id): -- This code is called on the URL PUT /inventories/<int:inventory_id>.
Used to update a Inventory. Input should be the inventory id to be updated.

    delete_inventories(inventory_id): -- This code is called on the URL DELETE /inventories/<int:inventory_id>. 
Used to delete a Inventory. Input should be the inventory id to be deleted.

    count_inventories_quantity(): -- This code is called on the URL GET /inventories/count.
Used to return a list of inventory. No input needed.

    query_inventories_by_name_status(): -- This code is called on the URL GET /inventories/query.
Used to query inventories by name and status. No input needed.
    
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
    

## Behavior Tests

This part is to do a behavior test, using Selenium automates browsers to simulate user actions, make sure every part on page works!

Do vagrant provision

    $ vagrant up && vagrant provision
    $ vagrant ssh

Add behavior test statements and step implementations in features folder and set up environment before Behavior Test

Start the server

    $ python run.py

Now you should be able to see the console page at: http://localhost:5000/

Run behavior test and see if tests pass in all senarios 

    $ behave 


## Swagger

We use a Flask plug-in called Flask-RESTPlus to imbed Swagger documentation into your Python Flask microservice so that the Swagger docs are generated.

Run the server with:
    
    $ python run.py

Finally you can see the microservice Swagger docs at: [http://localhost:5000/](http://localhost:5000/)

The front-end page will be at [http://localhost:5000/index.html](http://localhost:5000/index.html/)

## What's featured in the project?

    server.py -- the main Service using Python Flask
    test_server.py -- test cases using unittest
    test_inventories.py -- test cases using just the Inventory model
    models.py -- hold your model definitions of resource
