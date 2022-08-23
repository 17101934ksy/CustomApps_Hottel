from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from importlib import import_module
from sqlalchemy import MetaData

naming_convetion = {
    'ix' : "ix_%(column_0_label)s",
    'uq' : "uq_%(table_name)s_%(column_0_name)s",
    "ck" : "ck_%(table_name)s_%(column_0_name)s",
    "fk" : "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk" : "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convetion))
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)

    return app