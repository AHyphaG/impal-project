# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint
from .models import Users
from .Alamat import Alamat
from .Vehicles import Vehicles

blueprint = Blueprint(
    'authentication_blueprint',
    __name__,
    url_prefix=''
)
