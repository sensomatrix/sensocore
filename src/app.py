# src/app.py

from flask import Flask

from src.config import app_config
from src.models import db, bcrypt

from src.views.signal_view import signal_api as signal_blueprint
from src.views.device_view import device_api as device_blueprint
from src.views.patient_view import patient_api as patient_blueprint


def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)

    db.init_app(app)

    app.register_blueprint(signal_blueprint, url_prefix='/api/v1/signals')
    app.register_blueprint(device_blueprint, url_prefix='/api/v1/devices')
    app.register_blueprint(patient_blueprint, url_prefix='/api/v1/patients')

    return app
