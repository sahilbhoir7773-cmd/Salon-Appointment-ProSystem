from flask import Blueprint, render_template
from flask_login import login_required

from models.booking import Booking
from models.review import Review

report = Blueprint("report", __name__)


@report.route("/")
@login_required
def dashboard_report():

    total_bookings = Booking.query.count()

    pending = Booking.query.filter_by(
        status="Pending"
    ).count()

    accepted = Booking.query.filter_by(
        status="Accepted"
    ).count()

    completed = Booking.query.filter_by(
        status="Completed"
    ).count()

    rejected = Booking.query.filter_by(
        status="Rejected"
    ).count()

    bookings = Booking.query.filter_by(
        status="Completed"
    ).all()

    total_revenue = 0

    for booking in bookings:
        total_revenue += booking.service.price

    reviews = Review.query.all()

    if reviews:
        average_rating = round(
            sum(review.rating for review in reviews)
            / len(reviews),
            1
        )
    else:
        average_rating = 0

    return render_template(
        "owner/report.html",
        total_bookings=total_bookings,
        pending=pending,
        accepted=accepted,
        completed=completed,
        rejected=rejected,
        total_revenue=total_revenue,
        average_rating=average_rating
    )