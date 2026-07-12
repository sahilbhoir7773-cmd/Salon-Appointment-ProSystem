from flask import Blueprint, render_template
from flask_login import login_required
from models.booking import Booking

appointment = Blueprint("appointment", __name__)

@appointment.route("/")
@login_required
def appointments():

    bookings = Booking.query.order_by(
        Booking.booking_date.desc()
    ).all()

    return render_template(
        "owner/appointments.html",
        bookings=bookings
    )