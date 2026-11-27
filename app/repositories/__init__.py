import os
from sqlalchemy import text
from flask import Flask, redirect, url_for
from app.extensions import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Default configuration (overridden if test_config is passed by pytest)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key"),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'panther_parking.sqlite')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists for the SQLite file
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.lots import lots_bp
    from app.vehicles.routes import vehicles_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(lots_bp)
    app.register_blueprint(vehicles_bp)

    # Import models and create tables if they don't exist yet
    with app.app_context():
        from app.models import user, vehicle  # Ensures SQLAlchemy registers these models
        db.create_all()

        # Create the raw SQL tables (user / lot) if they aren't created by models
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'driver'
            )
        """))
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS lot (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                zone TEXT DEFAULT '',
                capacity INTEGER NOT NULL,
                total_spaces INTEGER NOT NULL,
                occupied INTEGER NOT NULL DEFAULT 0
            )
        """))
        db.session.commit()

    @app.route("/")
    def index():
        return redirect(url_for("lots.index"))

    return app