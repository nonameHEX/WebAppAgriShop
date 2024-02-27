from flask import Blueprint, render_template

import auth
from service.reservation_service import ReservationService

reservations = Blueprint("reservations", __name__)

@reservations.route('')
@auth.login_required
@auth.roles_required("Správce", "Dispečer")
def view_reservations_page():
    reservations = ReservationService.get_all()
    return render_template('reservations/reservation.jinja', reservations=reservations)