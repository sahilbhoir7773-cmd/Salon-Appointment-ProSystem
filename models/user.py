from datetime import datetime
from flask_login import UserMixin
from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(15),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="customer"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ---------------- Relationships ---------------- #

    salons = db.relationship(
        "Salon",
        back_populates="owner",
        lazy=True,
        cascade="all, delete-orphan"
    )

    bookings = db.relationship(
        "Booking",
        back_populates="customer",
        lazy=True,
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        back_populates="customer",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def is_admin(self):
        return self.role == "admin"

    def is_owner(self):
        return self.role == "owner"

    def is_customer(self):
        return self.role == "customer"

    def __repr__(self):
        return f"<User {self.full_name}>"
    
