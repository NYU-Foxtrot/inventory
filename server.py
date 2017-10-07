# Copyright 2016, 2017 John J. Rofrano. All Rights Reserved.
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
GET /inventories - Returns a list all of the Inventories
GET /inventories/{id} - Returns the Inventory with a given id number
POST /inventories - creates a new Inventory record in the database
PUT /inventories/{id} - updates a Inventory record in the database
DELETE /inventories/{id} - deletes a Inventory record in the database
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import NotFound
from models import Inventory, DataValidationError

# Create Flask application
app = Flask(__name__)

######################################################################
# Error Handlers
######################################################################

######################################################################
# GET INDEX
######################################################################

######################################################################
# LIST ALL INVENTORIES
######################################################################

######################################################################
# READ A INVENTORY
######################################################################

######################################################################
# CREATE A NEW INVENTORY
######################################################################

######################################################################
# UPDATE AN EXISTING INVENTORY
######################################################################

######################################################################
# DELETE A INVENTORY
######################################################################

######################################################################
# QUERY INVENTORIES
######################################################################

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    app.run()
