import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = "your_secret_key"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(BASE_DIR, "database", "salon.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail Configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_USERNAME = "your_email@gmail.com"
    MAIL_PASSWORD = "your_app_password"

    MAIL_DEFAULT_SENDER = "your_email@gmail.com"