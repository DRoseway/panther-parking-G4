from flask import Flask
from app.extensions import db as db_instance
from app.db import init_db

# Import model modules so SQLAlchemy registers both 'users' and 'vehicles' tables
from app.models import user, vehicle

def create_app(config_class=None):
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///panther_parking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'

    if config_class is not None:
        if isinstance(config_class, dict):
            app.config.from_mapping(config_class)
        else:
            app.config.from_object(config_class)

    # Initialize extensions
    db_instance.init_app(app)
    
    # NOTE: Removed init_db(app) here so tests can initialize tables dynamically with conftest.py

    # Register Blueprints
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.lots import bp as lots_bp
    app.register_blueprint(lots_bp, url_prefix='/lots')

    from app.vehicles.routes import vehicles_bp
    app.register_blueprint(vehicles_bp)

    return app