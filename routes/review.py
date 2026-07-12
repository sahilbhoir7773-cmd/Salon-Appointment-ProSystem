from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models.booking import Booking
from models.review import Review

review = Blueprint("review", __name__, url_prefix="/review")


# -----------------------------------
# Add Review
# -----------------------------------
@review.route("/add/<int:booking_id>", methods=["GET", "POST"])
@login_required
def add_review(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    # Only the customer who made the booking can review
    if booking.customer_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("booking.my_bookings"))

    # Allow review only for completed bookings
    if booking.status != "Completed":
        flash("You can review only completed bookings.", "warning")
        return redirect(url_for("booking.my_bookings"))

    # Prevent duplicate reviews
    existing_review = Review.query.filter_by(
        customer_id=current_user.id,
        salon_id=booking.service.salon_id
    ).first()

    if existing_review:
        flash("You have already reviewed this salon.", "info")
        return redirect(url_for("booking.my_bookings"))

    if request.method == "POST":

        new_review = Review(
            customer_id=current_user.id,
            salon_id=booking.service.salon_id,
            rating=int(request.form["rating"]),
            comment=request.form["comment"]
        )

        db.session.add(new_review)
        db.session.commit()

        flash("Review submitted successfully.", "success")

        return redirect(url_for("booking.my_bookings"))

    return render_template(
        "review/add_review.html",
        booking=booking
    )
