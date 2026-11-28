from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.services.vehicle_service import VehicleService
from app.models.vehicle import Vehicle

vehicles_bp = Blueprint('vehicles', __name__, url_prefix='/vehicles')


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if getattr(g, 'user', None) is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@vehicles_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    user_id = g.user['id']
    if request.method == 'POST':
        try:
            VehicleService.register_vehicle(request.form, user_id)
            flash('Vehicle registered successfully', 'success')
            return redirect(url_for('vehicles.register'))
        except ValueError as e:
            flash(str(e), 'danger')
            
    user_vehicles = Vehicle.query.filter_by(user_id=user_id).all()
    return render_template('vehicles/register.html', vehicles=user_vehicles)

@vehicles_bp.route('/delete/<plate>', methods=['POST'])
@login_required
def delete(plate):
    VehicleService.remove_vehicle(plate)
    flash('Vehicle removed', 'success')
    return redirect(url_for('vehicles.register'))