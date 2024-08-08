from flask import Blueprint, request, jsonify
import jwt
import bcrypt
from datetime import datetime, timedelta
from .models import create_user, get_user_by_email, verify_user
from .config import Config

auth_bp = Blueprint("auth", __name__)


# auth routes
def generate_token(user_id):
    expiration = datetime.utcnow() + timedelta(seconds=Config.JWT_EXPIRATION_DELTA)
    token = jwt.encode(
        {"sub": str(user_id), "exp": expiration}, Config.SECRET_KEY, algorithm="HS256"
    )
    return token


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"message": "Please provide all the information"}), 400

    name = name.strip()
    email = email.strip()
    password = password.strip()

    if get_user_by_email(email):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    create_user(name, email, hashed_password)
    return jsonify({"message": "User created successfully"}), 200


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Please provide email and password"}), 400

    email = email.strip()
    password = password.strip()

    user = verify_user(email, password)

    if user:
        token = generate_token(user["_id"])
        return (
            jsonify(
                {
                    "token": token,
                    "name": user["name"],
                }
            ),
            200,
        )

    return jsonify({"message": "Invalid credentials"}), 401
