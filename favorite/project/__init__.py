# -*- coding: utf-8 -*-
import os
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
# App initialisation
def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)
    # enable CORS
    CORS(app)
    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)
    # register endpoints 
    from project.api.favorite import favorite_blueprint
    app.favorite_blueprint(favorite_blueprint)
    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})
    return app
