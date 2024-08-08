import os
from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER_NAME = "uploaded_images"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_EXPIRATION_DELTA = int(
        os.getenv("JWT_EXPIRATION_DELTA", 3600 * 24 * 30)  # 30 day
    )

    UPLOAD_FOLDER_NAME = UPLOAD_FOLDER_NAME
    UPLOAD_FOLDER_PATH = os.path.join("app", "static", UPLOAD_FOLDER_NAME)
