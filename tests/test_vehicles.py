import pytest
from app import create_app
from app.extensions import db

def test_ac1_register_vehicle_success(client, register_and_login):
    """AC1: Given a logged-in user enters valid vehicle details, when submitted, it saves and displays."""
    register_and_login()
    response = client.post('/vehicles/register', data={
        'license_plate': 'XYZ-9876',
        'make': 'Honda',
        'model': 'Civic',
        'year': '2023',
        'color': 'Silver'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'XYZ-9876' in response.data
    assert b'Honda' in response.data

def test_ac2_duplicate_license_plate_rejected(client, register_and_login):
    """AC2: Given an existing license plate, when attempted to register again, system rejects with an error."""
    register_and_login()
    
    # Register the vehicle the first time
    client.post('/vehicles/register', data={
        'license_plate': 'DUPE-111',
        'make': 'Ford',
        'model': 'Focus',
        'year': '2020',
        'color': 'Black'
    }, follow_redirects=True)
    
    # Attempt to register the same license plate again
    response = client.post('/vehicles/register', data={
        'license_plate': 'DUPE-111',
        'make': 'Toyota',
        'model': 'Corolla',
        'year': '2022',
        'color': 'Red'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'License plate already registered' in response.data

def test_ac3_required_fields_validation(client, register_and_login):
    """AC3: Given required fields are blank, when submitted, form prevents submission and highlights error."""
    register_and_login()
    response = client.post('/vehicles/register', data={
        'license_plate': '',
        'make': '',
        'model': '',
        'year': '',
        'color': ''
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'required' in response.data.lower() or b'invalid' in response.data.lower()

def test_ac4_vehicle_removal(client, register_and_login):
    """AC4: Given a user views registered vehicles, when they click remove, the vehicle is deleted."""
    register_and_login()
    
    # First, register a vehicle to remove
    client.post('/vehicles/register', data={
        'license_plate': 'DEL-456',
        'make': 'Nissan',
        'model': 'Altima',
        'year': '2019',
        'color': 'White'
    }, follow_redirects=True)
    
    # Send a request to delete/remove the vehicle
    response = client.post('/vehicles/delete/DEL-456', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'DEL-456' not in response.data