from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db, bcrypt
from models.user import User

auth = Blueprint("auth", __name__)


# =========================
# Register
# =========================
@auth.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("home.index"))

    if request.method == "POST":

        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = request.form.get("role")

        # Password Match
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register"))

        # Email Exists
        existing_email = User.query.filter_by(email=email).first()

        if existing_email:
            flash("Email already exists.", "danger")
            return redirect(url_for("auth.register"))

        # Phone Exists
        existing_phone = User.query.filter_by(phone=phone).first()

        if existing_phone:
            flash("Phone number already exists.", "danger")
            return redirect(url_for("auth.register"))

        # Encrypt Password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Create User
        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            password=hashed_password,
            role=role
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful. Please Login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# =========================
# Login
# =========================
@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        if current_user.role == "owner":
            return redirect(url_for("owner.dashboard"))

        return redirect(url_for("customer.dashboard"))

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):

            login_user(user)

            flash("Login Successful.", "success")

            if user.role == "owner":
                return redirect(url_for("owner.dashboard"))

            return redirect(url_for("customer.dashboard"))

        flash("Invalid Email or Password.", "danger")

    return render_template("auth/login.html")


# =========================
# Logout
# =========================
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged Out Successfully.", "info")

    return redirect(url_for("home.index"))