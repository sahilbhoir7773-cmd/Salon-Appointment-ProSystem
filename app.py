from flask import Flask
from flask_login import LoginManager

from config import Config
from extensions import db

# Models
from models.user import User
from models.salon import Salon
from models.service import Service
from models.booking import Booking
from models.review import Review

# Blueprints
from routes.home import home
from routes.auth import auth
from routes.owner import owner
from routes.customer import customer
from routes.service import service
from routes.booking import booking
from routes.review import review
from routes.profile import profile
from routes.report import report


app = Flask(__name__)
app.config.from_object(Config)

# Initialize Extensions
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Register Blueprints
app.register_blueprint(home)
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(owner, url_prefix="/owner")
app.register_blueprint(customer, url_prefix="/customer")
app.register_blueprint(service, url_prefix="/service")
app.register_blueprint(booking, url_prefix="/booking")
app.register_blueprint(review, url_prefix="/review")
app.register_blueprint(profile, url_prefix="/profile")
app.register_blueprint(report, url_prefix="/report")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)

    