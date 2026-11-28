from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from ..services import lot_service

bp = Blueprint("lots", __name__, url_prefix="/lots")


def _can_manage_lots():
    if g.user is None:
        return False
    role = g.user.get("role", "driver")
    return role in ("admin", "manager", "driver")


@bp.route("/")
def index():
    return render_template(
        "lots.html",
        lots=lot_service.lots_with_status(),
        can_manage=_can_manage_lots(),
    )


@bp.route("/create", methods=("POST",))
def create():
    if not _can_manage_lots():
        flash("Please log in to manage parking lots.")
        return redirect(url_for("auth.login"))

    try:
        lot = lot_service.create_lot(
            name=request.form.get("name"),
            zone=request.form.get("zone"),
            capacity=request.form.get("capacity"),
            occupied=request.form.get("occupied", 0),
        )
        flash(f"Lot '{lot['name']}' created ({lot['status']}).")
    except ValueError as e:
        flash(str(e))

    return redirect(url_for("lots.index"))


@bp.route("/<int:lot_id>/update", methods=("POST",))
def update(lot_id):
    if not _can_manage_lots():
        flash("Please log in to manage parking lots.")
        return redirect(url_for("auth.login"))

    try:
        lot = lot_service.update_lot(
            lot_id=lot_id,
            capacity=request.form.get("capacity"),
            occupied=request.form.get("occupied"),
        )
        flash(f"Lot '{lot['name']}' updated ({lot['available']} available, {lot['status']}).")
    except ValueError as e:
        flash(str(e))

    return redirect(url_for("lots.index"))
