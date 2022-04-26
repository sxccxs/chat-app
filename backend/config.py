import os
from datetime import timedelta
from logging.config import fileConfig
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = os.environ.get("DATABASE_PORT")

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

ACTIVATION_EMAIL_PATH = Path("templates/account_activation_email.html")
PASSWORD_RESET_EMAIL_PATH = Path("templates/password_reset_email.html")

CONNECTION_STRING = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=12),
    "ALGORYTHM": "HS256",
}

origins = [
    "http://localhost:3000",
    "http://localhost:3000/*"
]

# fileConfig("./logging.conf")
