# # -*- encoding: utf-8 -*-
# """
# Copyright (c) 2019 - present AppSeed.us
# """

# import os
# from   flask_migrate import Migrate
# from   flask_minify  import Minify
# from   sys import exit

# from apps.config import config_dict
# from apps import create_app, db

# from flask_wtf.csrf import CSRFProtect

# # WARNING: Don't run with debug turned on in production!
# DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# # The configuration
# get_config_mode = 'Debug' if DEBUG else 'Production'

# try:

#     # Load the configuration using the default values
#     app_config = config_dict[get_config_mode.capitalize()]

# except KeyError:
#     exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

# flask_app = create_app(app_config)
# celery_app = flask_app.extensions["celery"]


# import os
# from flask_migrate import Migrate
# from sys import exit
# from apps.config import config_dict
# from apps import create_app, db

# # Hapus semua environment variables database yang mungkin ada
# for key in ['DB_ENGINE', 'DB_USERNAME', 'DB_PASS', 'DB_HOST', 'DB_PORT', 'DB_NAME']:
#     if key in os.environ:
#         del os.environ[key]

# # Set environment variables baru
# os.environ.update({
#     'DB_ENGINE': 'mysql+mysqldb',  # atau mysql+pymysql
#     'DB_USERNAME': 'root',         # sesuaikan
#     'DB_PASS': 'admin',                 # sesuaikan
#     'DB_HOST': 'localhost',
#     'DB_PORT': '3306',
#     'DB_NAME': 'mokel'            # sesuaikan
# })

# # Print current environment
# print("Current environment variables:")
# for key in ['DB_ENGINE', 'DB_USERNAME', 'DB_PASS', 'DB_HOST', 'DB_PORT', 'DB_NAME']:
#     print(f"{key}: {os.environ.get(key)}")

# DEBUG = False  # Force production mode
# get_config_mode = 'Production'  # Force production config

# try:
#     app_config = config_dict[get_config_mode]
# except KeyError:
#     exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

# # Create Flask app
# flask_app = create_app(app_config)

# # Force MySQL configuration
# flask_app.config['SQLALCHEMY_DATABASE_URI'] = (
#     f"mysql+mysqldb://root:@localhost:3306/mokel"  # sesuaikan
# )
# flask_app.config['USE_SQLITE'] = False

# print(f"Final Database URI: {flask_app.config['SQLALCHEMY_DATABASE_URI']}")

# # Initialize app context
# flask_app.app_context().push()

# # Test database connection
# try:
#     with flask_app.app_context():
#         result = db.session.execute('SELECT 1').scalar()
#         print("Database connection test successful")
# except Exception as e:
#     print(f"Database connection failed: {e}")

# celery_app = flask_app.extensions["celery"]


import os
from flask_migrate import Migrate
from sys import exit
from apps.config import config_dict
from apps import create_app, db

# Set environment variables dengan credentials yang benar
os.environ.update({
    'DB_ENGINE': 'mysql+mysqldb',
    'DB_USERNAME': 'root',
    'DB_PASS': '',         # password yang benar
    'DB_HOST': 'localhost',
    'DB_PORT': '3306',
    'DB_NAME': 'mokel'
})
# # Print current environment
print("Current environment variables:")
for key in ['DB_ENGINE', 'DB_USERNAME', 'DB_PASS', 'DB_HOST', 'DB_PORT', 'DB_NAME']:
    print(f"{key}: {os.environ.get(key)}")
    
DEBUG = False
get_config_mode = 'Production'

try:
    app_config = config_dict[get_config_mode]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

# Create Flask app
flask_app = create_app(app_config)

# Force MySQL configuration dengan credentials yang benar
flask_app.config['SQLALCHEMY_DATABASE_URI'] = (
    # Kalau pake password yang di bawah
    # f"mysql+mysqldb://root:admin@localhost:3306/mokel"
    # Kalau tidak pake yang dibawah
    f"mysql+mysqldb://root@localhost:3306/mokel"
)
flask_app.config['USE_SQLITE'] = False

print(f"Final Database URI: {flask_app.config['SQLALCHEMY_DATABASE_URI']}")

flask_app.app_context().push()

# Test database connection
try:
    with flask_app.app_context():
        result = db.session.execute('SELECT 1').scalar()
        print("Database connection test successful")
except Exception as e:
    print(f"Database connection failed: {e}")

celery_app = flask_app.extensions["celery"]