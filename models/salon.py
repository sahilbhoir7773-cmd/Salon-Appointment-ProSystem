from datetime import datetime
from extensions import db


class Salon(db.Model):
    __tablename__ = "salons"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    salon_name = db.Column(
        db.String(100),
        nullable=False
    )

    address = db.Column(
        db.String(200),
        nullable=False
    )

    city = db.Column(
        db.String(100),
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    opening_time = db.Column(
        db.String(20)
    )

    closing_time = db.Column(
        db.String(20)
    )

    description = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(200)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ---------------- Relationships ---------------- #

    owner = db.relationship(
        "User",
        back_populates="salons"
    )

    services = db.relationship(
        "Service",
        back_populates="salon",
        lazy=True,
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        back_populates="salon",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Salon {self.salon_name}>"