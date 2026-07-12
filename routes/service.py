from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models.service import Service
from models.salon import Salon

service = Blueprint("service", __name__, url_prefix="/service")


# ---------------------------------
# List Services
# ---------------------------------
@service.route("/")
@login_required
def list_services():

    salon = Salon.query.filter_by(owner_id=current_user.id).first()

    if salon is None:
        flash("Please add your salon first.", "warning")
        return redirect(url_for("owner.add_salon"))

    services = Service.query.filter_by(salon_id=salon.id).all()

    return render_template(
        "service/list.html",
        services=services
    )


# ---------------------------------
# Add Service
# ---------------------------------
@service.route("/add", methods=["GET", "POST"])
@login_required
def add_service():

    salon = Salon.query.filter_by(owner_id=current_user.id).first()

    if salon is None:
        flash("Please add your salon first.", "warning")
        return redirect(url_for("owner.add_salon"))

    if request.method == "POST":

        new_service = Service(
            salon_id=salon.id,
            service_name=request.form["service_name"],
            description=request.form.get("description"),
            price=float(request.form["price"]),
            duration=int(request.form["duration"])
        )

        db.session.add(new_service)
        db.session.commit()

        flash("Service added successfully.", "success")
        return redirect(url_for("service.list_services"))

    return render_template("service/add.html")


# ---------------------------------
# Edit Service
# ---------------------------------
@service.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_service(id):

    service_obj = Service.query.get_or_404(id)

    salon = Salon.query.filter_by(owner_id=current_user.id).first()

    if salon is None or service_obj.salon_id != salon.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("owner.dashboard"))

    if request.method == "POST":

        service_obj.service_name = request.form["service_name"]
        service_obj.description = request.form.get("description")
        service_obj.price = float(request.form["price"])
        service_obj.duration = int(request.form["duration"])

        db.session.commit()

        flash("Service updated successfully.", "success")
        return redirect(url_for("service.list_services"))

    return render_template(
        "service/edit.html",
        service=service_obj
    )


# ---------------------------------
# Delete Service
# ---------------------------------
@service.route("/delete/<int:id>")
@login_required
def delete_service(id):

    service_obj = Service.query.get_or_404(id)

    salon = Salon.query.filter_by(owner_id=current_user.id).first()

    if salon is None or service_obj.salon_id != salon.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("owner.dashboard"))

    db.session.delete(service_obj)
    db.session.commit()

    flash("Service deleted successfully.", "success")

    return redirect(url_for("service.list_services"))