from sqlalchemy import text
from app.db import get_db


def _has_zone_column(db):
    cols = db.execute(text("PRAGMA table_info(lot)")).fetchall()
    return any(col[1] == "zone" for col in cols)


def list_all():
    rows = get_db().execute(text("SELECT * FROM lot ORDER BY name")).fetchall()
    return [dict(row._mapping) for row in rows]


def find_by_id(lot_id):
    row = get_db().execute(
        text("SELECT * FROM lot WHERE id = :lot_id"),
        {"lot_id": lot_id},
    ).fetchone()
    return dict(row._mapping) if row else None


def find_by_name(name):
    row = get_db().execute(
        text("SELECT * FROM lot WHERE LOWER(name) = LOWER(:name)"),
        {"name": name},
    ).fetchone()
    return dict(row._mapping) if row else None


def create(name, zone, capacity, occupied=0):
    db = get_db()
    if _has_zone_column(db):
        cur = db.execute(
            text(
                "INSERT INTO lot (name, zone, capacity, total_spaces, occupied) "
                "VALUES (:name, :zone, :capacity, :total_spaces, :occupied)"
            ),
            {
                "name": name,
                "zone": zone or "",
                "capacity": capacity,
                "total_spaces": capacity,
                "occupied": occupied,
            },
        )
    else:
        cur = db.execute(
            text(
                "INSERT INTO lot (name, capacity, total_spaces, occupied) "
                "VALUES (:name, :capacity, :total_spaces, :occupied)"
            ),
            {
                "name": name,
                "capacity": capacity,
                "total_spaces": capacity,
                "occupied": occupied,
            },
        )
    db.commit()
    return find_by_id(cur.lastrowid)


def update_capacity_and_occupancy(lot_id, capacity, occupied):
    db = get_db()
    db.execute(
        text(
            "UPDATE lot "
            "SET capacity = :capacity, total_spaces = :total_spaces, occupied = :occupied "
            "WHERE id = :lot_id"
        ),
        {
            "lot_id": lot_id,
            "capacity": capacity,
            "total_spaces": capacity,
            "occupied": occupied,
        },
    )
    db.commit()
    return find_by_id(lot_id)
