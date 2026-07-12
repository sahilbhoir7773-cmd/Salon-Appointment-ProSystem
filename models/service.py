from extensions import db


class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)

    salon_id = db.Column(
        db.Integer,
        db.ForeignKey("salons.id"),
        nullable=False
    )

    service_name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(db.Text)

    price = db.Column(
        db.Float,
        nullable=False
    )

    duration = db.Column(
        db.Integer,
        nullable=False
    )

    salon = db.relationship(
        "Salon",
        back_populates="services"
    )

    bookings = db.relationship(
        "Booking",
        back_populates="service",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Service {self.service_name}>"