from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required
from flask_login import current_user

from extensions import db

from models.user import User
from models.salon import Salon
from models.service import Service
from models.booking import Booking

admin = Blueprint("admin", __name__)

@admin.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "admin":
        flash("Access Denied", "danger")
        return redirect(url_for("home.index"))

    total_users = User.query.count()
    total_salons = Salon.query.count()
    total_services = Service.query.count()
    total_bookings = Booking.query.count()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_salons=total_salons,
        total_services=total_services,
        total_bookings=total_bookings
    )

@admin.route("/users")
@login_required
def users():

    if current_user.role != "admin":
        flash("Access Denied", "danger")
        return redirect(url_for("home.index"))

    users = User.query.all()

    return render_template(
        "admin/users.html",
        users=users
    )

@admin.route("/delete-user/<int:id>")
@login_required
def delete_user(id):

    if current_user.role != "admin":
        flash("Access Denied", "danger")
        return redirect(url_for("home.index"))

    user = User.query.get_or_404(id)

    if user.id == current_user.id:
        flash("You cannot delete your own account.", "warning")
        return redirect(url_for("admin.users"))

    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully.", "success")

    return redirect(url_for("admin.users"))

@admin.route("/salons")
@login_required
def salons():

    if current_user.role != "admin":
        flash("Access Denied", "danger")
        return redirect(url_for("home.index"))

    salons = Salon.query.all()

    return render_template(
        "admin/salons.html",
        salons=salons
    )

@admin.route("/delete-salon/<int:id>")
@login_required
def delete_salon(id):

    if current_user.role != "admin":
        flash("Access Denied", "danger")
        return redirect(url_for("home.index"))

    salon = Salon.query.get_or_404(id)

    db.session.delete(salon)
    db.session.commit()

    flash("Salon deleted successfully.", "success")

    return redirect(url_for("admin.salons"))

@admin.route("/bookings")
@login_required
def bookings():

    if current_user.role != "admin":
        flash("Access Denied", "danger")
        return redirect(url_for("home.index"))

    bookings = Booking.query.all()

    return render_template(
        "admin/bookings.html",
        bookings=bookings
    )

