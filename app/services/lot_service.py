"""Business rules for parking lots."""
from ..repositories import lot_repository

FILLING_THRESHOLD = 0.75  # 75% occupied or more = "filling"


def status_for(capacity, occupied):
    """Return 'open', 'filling' or 'full' for a lot.

    Story #5 acceptance criteria live in tests/test_lots.py.
    """
    if occupied >= capacity:
        return "full"
    if occupied / capacity >= FILLING_THRESHOLD:
        return "filling"
    return "open"


def _enrich_lot(lot):
    lot["status"] = status_for(lot["capacity"], lot["occupied"])
    lot["available"] = max(lot["capacity"] - lot["occupied"], 0)
    lot.setdefault("zone", "")
    return lot


def lots_with_status():
    lots = lot_repository.list_all()
    return [_enrich_lot(lot) for lot in lots]


def create_lot(name, zone, capacity, occupied=0):
    clean_name = (name or "").strip()
    clean_zone = (zone or "").strip()

    if not clean_name:
        raise ValueError("Lot name is required.")

    try:
        cap = int(capacity)
        occ = int(occupied if occupied not in (None, "") else 0)
    except (TypeError, ValueError):
        raise ValueError("Capacity and occupied spaces must be whole numbers.")

    if cap <= 0:
        raise ValueError("Total capacity must be greater than zero.")
    if occ < 0 or occ > cap:
        raise ValueError("Occupied spaces must be between 0 and total capacity.")

    if lot_repository.find_by_name(clean_name):
        raise ValueError("Lot name already exists")

    created = lot_repository.create(clean_name, clean_zone, cap, occ)
    return _enrich_lot(created)


def update_lot(lot_id, capacity, occupied):
    existing = lot_repository.find_by_id(lot_id)
    if not existing:
        raise ValueError("Parking lot not found.")

    try:
        cap = int(capacity)
        occ = int(occupied)
    except (TypeError, ValueError):
        raise ValueError("Capacity and occupied spaces must be whole numbers.")

    if cap <= 0:
        raise ValueError("Total capacity must be greater than zero.")
    if occ < 0 or occ > cap:
        raise ValueError("Occupied spaces must be between 0 and total capacity.")

    updated = lot_repository.update_capacity_and_occupancy(lot_id, cap, occ)
    return _enrich_lot(updated)
