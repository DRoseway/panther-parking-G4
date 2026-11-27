from sqlalchemy import text
from app.db import get_db

def list_all():
    rows = get_db().execute(text("SELECT * FROM lot ORDER BY name")).fetchall()
    return [dict(row._mapping) for row in rows]