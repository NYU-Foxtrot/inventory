"""
Microservice module

This module contains the microservice code for
    server
    models
"""
from flask import Flask

# Create the Flask app
app = Flask(__name__)
app.config.from_object('config')

import server
import models