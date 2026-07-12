from datetime import datetime
from extensions import db


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    salon_id = db.Column(
        db.Integer,
        db.ForeignKey("salons.id"),
        nullable=False
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    comment = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    customer = db.relationship(
        "User",
        back_populates="reviews"
    )

    salon = db.relationship(
        "Salon",
        back_populates="reviews"
    )

    def __repr__(self):
        return f"<Review {self.id}>"