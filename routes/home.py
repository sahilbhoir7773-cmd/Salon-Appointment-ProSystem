from flask import Blueprint, render_template
from models.service import Service
from models.review import Review

home = Blueprint("home", __name__)

@home.route("/")
def index():

    services = Service.query.all()

    reviews = Review.query.order_by(
        Review.id.desc()
    ).limit(6).all()

    return render_template(
        "index.html",
        services=services,
        reviews=reviews
    )
