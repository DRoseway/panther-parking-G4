import pytest
from app import create_app
from app.extensions import db
from sqlalchemy.pool import StaticPool
from sqlalchemy import text

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_ENGINE_OPTIONS": {
            "poolclass": StaticPool,
            "connect_args": {"check_same_thread": False}
        },
        "SECRET_KEY": "test"
    })
    
    with app.app_context():
        # Explicitly import models so their metadata attaches to db
        from app.models.user import User
        from app.models.vehicle import Vehicle
        
        db.drop_all()
        db.create_all()
        
        # Create raw SQL table for lots
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS lot (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                capacity INTEGER NOT NULL,
                total_spaces INTEGER NOT NULL,
                occupied INTEGER NOT NULL DEFAULT 0
            )
        """))

        # Seed the default lot expected by test_ac4_lots_page_lists_lots
        db.session.execute(text("""
            INSERT INTO lot (name, capacity, total_spaces, occupied)
            VALUES ('Lot 1 - Memorial Student Center', 220, 220, 40)
        """))

        db.session.commit()
        
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def register_and_login(client):
    def _do(email="student@pvamu.edu", password="panthers123"):
        client.post("/auth/register", data={"email": email, "password": password})
        return client.post("/auth/login", data={"email": email, "password": password})
    return _do