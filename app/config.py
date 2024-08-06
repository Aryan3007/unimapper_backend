import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_EXPIRATION_DELTA = int(
        os.getenv("JWT_EXPIRATION_DELTA", 3600 * 24 * 30)  # 30 day
    )
