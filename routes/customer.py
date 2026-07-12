from flask import Blueprint, render_template
from flask_login import login_required,current_user

from models.salon import Salon
from models.service import Service
from models.booking import Booking

customer = Blueprint("customer", __name__)


# -----------------------------
# Customer Dashboard
# -----------------------------
@customer.route("/dashboard")
@login_required
def dashboard():

    # Get the first (and only) salon
    salon = Salon.query.first()

    services = []

    if salon:
        services = Service.query.filter_by(
            salon_id=salon.id
        ).all()

    return render_template(
        "customer/dashboard.html",
        salon=salon,
        services=services
    )


# -----------------------------
# Booking History
# -----------------------------
@customer.route("/history")
@login_required
def history():

    bookings = Booking.query.filter_by(
        customer_id=current_user.id
    ).all()

    return render_template(
        "customer/history.html",
        bookings=bookings
    )

