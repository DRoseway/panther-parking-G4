from app.extensions import db

def init_db(app=None):
    """Initialize database tables within context if needed."""
    if app is not None:
        with app.app_context():
            db.create_all()
    else:
        db.create_all()

def get_db():
    """Return the active SQLAlchemy session for command execution."""
    return db.session