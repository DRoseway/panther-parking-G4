from sqlalchemy import text
from app.db import get_db

def find_by_email(email):
    row = get_db().execute(
        text("SELECT * FROM user WHERE email = :email"), 
        {"email": email}
    ).fetchone()
    return dict(row._mapping) if row else None

def find_by_id(user_id):
    row = get_db().execute(
        text("SELECT * FROM user WHERE id = :user_id"), 
        {"user_id": user_id}
    ).fetchone()
    return dict(row._mapping) if row else None

def create(email, password_hash, role="driver"):
    db = get_db()
    cur = db.execute(
        text("INSERT INTO user (email, password_hash, role) VALUES (:email, :password_hash, :role)"),
        {"email": email, "password_hash": password_hash, "role": role}
    )
    db.commit()
    return cur.lastrowid