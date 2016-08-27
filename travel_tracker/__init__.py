#! ../env/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Karthik Hariharan'
__email__ = 'karthikhariharan13@gmail.com'
__version__ = '0.1'

from flask import Flask
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.social import Social
from flask.ext.social.datastore import SQLAlchemyConnectionDatastore
from webassets.loaders import PythonLoader as PythonAssetsLoader

from travel_tracker.controllers.main import main
from travel_tracker import assets, models, forms
from travel_tracker.models import db

from travel_tracker.extensions import (
    cache,
    assets_env,
    debug_toolbar,
)


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. travel_tracker.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)

    app.config.from_object('travel_tracker.settings')

    # initialize the cache
    cache.init_app(app)

    # initialize the debug tool bar
    debug_toolbar.init_app(app)

    # initialize SQLAlchemy
    db.init_app(app)

    app.config['SOCIAL_FACEBOOK'] = {
        'consumer_key': '697982927020266',
        'consumer_secret': '34da971ebd7ba29c045f003ddc0f368d'
    }

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    # register our blueprints
    app.register_blueprint(main)

    # initialize flask security and social
    security_ds = SQLAlchemyUserDatastore(db, models.User, models.Role)
    social_ds = SQLAlchemyConnectionDatastore(db, models.Connection)

    app.security = Security(app, security_ds, register_form=forms.ExtendedRegisterForm)
    app.social = Social(app, social_ds)

    return app
