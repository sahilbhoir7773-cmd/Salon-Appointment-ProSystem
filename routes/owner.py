from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models.salon import Salon
from models.service import Service
from models.review import Review
from models.booking import Booking

owner = Blueprint("owner", __name__, url_prefix="/owner")


# -------------------------
# Owner Dashboard
# -------------------------
@owner.route("/dashboard")
@login_required
def dashboard():

    salon = Salon.query.filter_by(owner_id=current_user.id).first()

    services = []
    reviews = []
    bookings = []

    if salon:
        services = Service.query.filter_by(salon_id=salon.id).all()
        reviews = Review.query.filter_by(salon_id=salon.id).all()

        service_ids = [service.id for service in services]

        if service_ids:
            bookings = Booking.query.filter(
                Booking.service_id.in_(service_ids)
            ).all()

    return render_template(
        "owner/dashboard.html",
        salon=salon,
        services=services,
        reviews=reviews,
        bookings=bookings
    )


# -------------------------
# Add Salon
# -------------------------
@owner.route("/add-salon", methods=["GET", "POST"])
@login_required
def add_salon():

    salon = Salon.query.filter_by(owner_id=current_user.id).first()

    if salon:
        flash("You already have a salon.", "warning")
        return redirect(url_for("owner.dashboard"))

    if request.method == "POST":

        salon = Salon(
            owner_id=current_user.id,
            salon_name=request.form["salon_name"],
            address=request.form["address"],
            city=request.form["city"],
            phone=request.form["phone"],
            opening_time=request.form["opening_time"],
            closing_time=request.form["closing_time"],
            description=request.form["description"]
        )

        db.session.add(salon)
        db.session.commit()

        flash("Salon Added Successfully!", "success")
        return redirect(url_for("owner.dashboard"))

    return render_template("owner/add_salon.html")


# -------------------------
# Add Service
# -------------------------
@owner.route("/add-service", methods=["GET", "POST"])
@login_required
def add_service():

    salon = Salon.query.filter_by(owner_id=current_user.id).first()

    if not salon:
        flash("Please add your salon first.", "warning")
        return redirect(url_for("owner.add_salon"))

    if request.method == "POST":

        service = Service(
            salon_id=salon.id,
            service_name=request.form["service_name"],
            description=request.form["description"],
            price=request.form["price"],
            duration=request.form["duration"]
        )

        db.session.add(service)
        db.session.commit()

        flash("Service Added Successfully!", "success")
        return redirect(url_for("owner.dashboard"))

    return render_template("owner/add_service.html")


# -------------------------
# Owner Reviews
# -------------------------
@owner.route("/reviews")
@login_required
def reviews():

    salon = Salon.query.filter_by(owner_id=current_user.id).first()

    if not salon:
        flash("Please add your salon first.", "warning")
        return redirect(url_for("owner.dashboard"))

    reviews = Review.query.filter_by(
        salon_id=salon.id
    ).all()

    return render_template(
        "owner/reviews.html",
        reviews=reviews
    )


# -------------------------
# Owner Bookings
# -------------------------
@owner.route("/bookings")
@login_required
def bookings():

    salon = Salon.query.filter_by(owner_id=current_user.id).first()

    if not salon:
        flash("Please add your salon first.", "warning")
        return redirect(url_for("owner.dashboard"))

    services = Service.query.filter_by(
        salon_id=salon.id
    ).all()

    service_ids = [service.id for service in services]

    bookings = Booking.query.filter(
        Booking.service_id.in_(service_ids)
    ).all()

    return render_template(
        "owner/bookings.html",
        bookings=bookings
    )


# -------------------------
# Approve Booking
# -------------------------
@owner.route("/approve-booking/<int:id>")
@login_required
def approve_booking(id):

    booking = Booking.query.get_or_404(id)

    booking.status = "Approved"

    db.session.commit()

    flash("Booking Approved Successfully!", "success")

    return redirect(url_for("owner.bookings"))


# -------------------------
# Complete Booking
# -------------------------
@owner.route("/complete-booking/<int:id>")
@login_required
def complete_booking(id):

    booking = Booking.query.get_or_404(id)

    booking.status = "Completed"

    db.session.commit()

    flash("Booking Completed Successfully!", "success")

    return redirect(url_for("owner.bookings"))
