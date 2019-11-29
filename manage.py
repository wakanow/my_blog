import sys
import os
import click
# from flask_migrate import Migrate, upgrade
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# migrate = Migrate(app, db)
