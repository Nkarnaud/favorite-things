# -*- coding: utf-8 -*-
import os
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()


# App initialisation
def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)
    # set config instance_relative_config=True
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    #app.config.from_pyfile('config.py')
    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)
    app.logger
    # register endpoints 
    from project.api.favorite import favorite_blueprint
    app.register_blueprint(favorite_blueprint)
    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})
    return app
