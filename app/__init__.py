"""
Microservice module

This module contains the microservice code for
    service
    models
"""
from flask import Flask

# Create the Flask aoo
app = Flask(__name__)
app.config.from_object('config')

# Load Configurations
#app.config.from_object('config')

import server
import models