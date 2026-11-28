from app.repositories.vehicle_repository import VehicleRepository
from app.models.vehicle import Vehicle

class VehicleService:
    @staticmethod
    def register_vehicle(data, user_id):
        plate = data.get('license_plate')
        if not plate or not data.get('make') or not data.get('model'):
            raise ValueError("Required fields are missing.")
            
        if VehicleRepository.find_by_plate(plate):
            raise ValueError("License plate already registered")
            
        vehicle = Vehicle(
            license_plate=plate,
            make=data.get('make'),
            model=data.get('model'),
            year=int(data.get('year') or 0),
            color=data.get('color'),
            user_id=user_id
        )
        VehicleRepository.save(vehicle)
        return vehicle

    @staticmethod
    def remove_vehicle(license_plate):
        return VehicleRepository.delete_by_plate(license_plate)