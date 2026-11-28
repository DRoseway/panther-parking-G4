from ..db import get_db
from app.extensions import db
from app.models.vehicle import Vehicle

class VehicleRepository:
    @staticmethod
    def save(vehicle):
        db.session.add(vehicle)
        db.session.commit()

    @staticmethod
    def find_by_plate(license_plate):
        return Vehicle.query.filter_by(license_plate=license_plate).first()




    @staticmethod
    def get_by_user_id(user_id):
        return Vehicle.query.filter_by(user_id=user_id).all()
        
    @staticmethod
    def delete_by_plate(license_plate):
        vehicle = Vehicle.query.filter_by(license_plate=license_plate).first()
        if vehicle:
            db.session.delete(vehicle)
            db.session.commit()
        return vehicle