from flask import Blueprint, render_template
from flask_login import login_required

profile = Blueprint("profile", __name__)


@profile.route("/")
@login_required
def edit_profile():
    return render_template("owner/profile.html")