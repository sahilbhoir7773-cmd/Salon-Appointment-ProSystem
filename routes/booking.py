from datetime import datetime, date

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models.booking import Booking
from models.service import Service

booking = Blueprint("booking", __name__, url_prefix="/booking")


# -----------------------------
# Book Appointment
# -----------------------------
@booking.route("/book/<int:service_id>", methods=["GET", "POST"])
@login_required
def book(service_id):

    service = Service.query.get_or_404(service_id)

    if request.method == "POST":

        booking_date = datetime.strptime(
            request.form["booking_date"],
            "%Y-%m-%d"
        ).date()

        booking_time = request.form["booking_time"]

        if booking_date < date.today():
            flash("You cannot book a past date.", "danger")
            return redirect(url_for("booking.book", service_id=service.id))

        new_booking = Booking(
            customer_id=current_user.id,
            service_id=service.id,
            booking_date=booking_date,
            booking_time=booking_time,
            status="Pending"
        )

        db.session.add(new_booking)
        db.session.commit()

        flash("Appointment booked successfully!", "success")
        return redirect(url_for("booking.my_bookings"))

    return render_template(
        "booking/book.html",
        service=service
    )


# -----------------------------
# My Bookings
# -----------------------------
@booking.route("/my-bookings")
@login_required
def my_bookings():

    bookings = Booking.query.filter_by(
        customer_id=current_user.id
    ).order_by(
        Booking.booking_date.desc()
    ).all()

    return render_template(
        "booking/my_bookings.html",
        bookings=bookings
    )


# -----------------------------
# Booking History
# -----------------------------
@booking.route("/history")
@login_required
def history():

    bookings = Booking.query.filter_by(
        customer_id=current_user.id
    ).order_by(
        Booking.booking_date.desc()
    ).all()

    return render_template(
        "booking/history.html",
        bookings=bookings
    )


# -----------------------------
# Cancel Booking
# -----------------------------
@booking.route("/cancel/<int:id>")
@login_required
def cancel_booking(id):

    booking = Booking.query.get_or_404(id)

    if booking.customer_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("booking.my_bookings"))

    if booking.status != "Pending":
        flash("Only pending bookings can be cancelled.", "warning")
        return redirect(url_for("booking.my_bookings"))

    booking.status = "Cancelled"

    db.session.commit()

    flash("Booking cancelled successfully.", "success")

    return redirect(url_for("booking.my_bookings"))