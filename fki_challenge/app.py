# -*- coding: utf-8 -*-

"""
fki_challenge.app
~~~~~~~~~~~~~~~~~

Our web RESTful API.
"""

from flask import Flask
from flask_restful import Api
from . import models, resources


def _db_connect():
    models.database.connect()


def _db_close(exception):
    if not models.database.is_closed():
        models.database.close()


def create_app(settings_override=None):
    """Returns a `Flask` application instance configured.
    """

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('fki_challenge.settings')
    app.config.from_pyfile('application.cfg', silent=True)
    app.config.from_object(settings_override)

    api = Api(app, prefix='/api', catch_all_404s=True)

    # ensure tables
    models.database.init(app.config['FKI_DATABASE_FILE'])
    models.database.connect()
    models.database.create_tables([models.Attribute, models.Person, models.PersonAttribute],
                                  safe=True)

    # register db request hooks
    app.before_request(_db_connect)
    app.teardown_request(_db_close)

    # wire resources
    api.add_resource(resources.Attribute, '/attributes/<int:attribute_id>')
    api.add_resource(resources.AttributeList, '/attributes/')
    api.add_resource(resources.Person, '/persons/<int:person_id>')
    api.add_resource(resources.PersonList, '/persons/')
    api.add_resource(resources.MatchList, '/matches/',
                     resource_class_kwargs={'error_rate': app.config['FKI_ERROR_RATE']})

    return app
