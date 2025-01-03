# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit

from apps.config import config_dict
from apps import create_app, db

from flask_wtf.csrf import CSRFProtect

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

# app = create_app(app_config)
app = create_app(app_config)
Migrate(app, db)
celery_app = app.extensions["celery"]
if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)
    
if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG)             )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT )

csrf = CSRFProtect(app)

@app.template_filter('currency')
def format_currency(value):
    """Format angka menjadi IDR"""
    try:
        return "Rp{:,.0f}".format(float(value)).replace(',', '.')
    except ValueError:
        return value

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5005")
# test farrel