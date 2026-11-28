"""Story #5 & Issue #3 (Manage Lots): Parking lot capacity, status, creation, and updates."""
from app.services.lot_service import lots_with_status, status_for


def test_ac1_open():
    assert status_for(capacity=100, occupied=74) == "open"


def test_ac2_filling_at_threshold():
    assert status_for(capacity=100, occupied=75) == "filling"
    assert status_for(capacity=100, occupied=99) == "filling"


def test_ac3_full():
    assert status_for(capacity=100, occupied=100) == "full"
    assert status_for(capacity=100, occupied=105) == "full"


def test_ac4_lots_page_lists_lots(client):
    resp = client.get("/lots/")
    assert resp.status_code == 200
    assert b"Lot 1 - Memorial Student Center" in resp.data
    assert b"180 of 220" in resp.data


def test_manage_lots_ac1_create_new_lot(client, register_and_login):
    register_and_login()
    resp = client.post(
        "/lots/create",
        data={"name": "Lot 2 - North Deck", "zone": "North Campus", "capacity": 150, "occupied": 0},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Lot 2 - North Deck" in resp.data
    assert b"150 of 150" in resp.data
    assert b"open" in resp.data


def test_manage_lots_ac2_update_capacity_and_occupancy(client, register_and_login):
    register_and_login()
    # Seeded Lot 1 has id=1, capacity=220, occupied=40
    resp = client.post(
        "/lots/1/update",
        data={"capacity": 200, "occupied": 50},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"150 of 200" in resp.data
    assert b"open" in resp.data


def test_manage_lots_ac3_duplicate_lot_name_rejected(client, register_and_login):
    register_and_login()
    resp = client.post(
        "/lots/create",
        data={"name": "Lot 1 - Memorial Student Center", "zone": "Central", "capacity": 100},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Lot name already exists" in resp.data


def test_manage_lots_ac4_status_threshold_trigger(client, register_and_login):
    register_and_login()
    # Shift Lot 1 (capacity 200) to 90% full (180 occupied) -> filling
    resp_filling = client.post(
        "/lots/1/update",
        data={"capacity": 200, "occupied": 180},
        follow_redirects=True,
    )
    assert resp_filling.status_code == 200
    assert b"filling" in resp_filling.data

    # Shift Lot 1 to 100% capacity (200 occupied) -> full
    resp_full = client.post(
        "/lots/1/update",
        data={"capacity": 200, "occupied": 200},
        follow_redirects=True,
    )
    assert resp_full.status_code == 200
    assert b"full" in resp_full.data