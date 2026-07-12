from datetime import datetime
from extensions import db


class Booking(db.Model):

    __tablename__ = "bookings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    service_id = db.Column(
        db.Integer,
        db.ForeignKey("services.id"),
        nullable=False
    )

    booking_date = db.Column(
        db.Date,
        nullable=False
    )

    booking_time = db.Column(
        db.String(20),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationships

    customer = db.relationship(
        "User",
        back_populates="bookings"
    )

    service = db.relationship(
        "Service",
        back_populates="bookings"
    )

    def __repr__(self):
        return f"<Booking {self.id}>"