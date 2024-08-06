from flask_pymongo import PyMongo
from flask import current_app
import bcrypt

mongo = PyMongo()


def init_db(app):
    mongo.init_app(app)


def get_user_by_email(email):
    return mongo.db.users.find_one({"email": email})


def create_user(name, email, hashed_password):
    mongo.db.users.insert_one(
        {"name": name, "email": email, "password": hashed_password}
    )


def verify_user(email, password):
    user = get_user_by_email(email)
    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return user
    return None
