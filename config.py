import os
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).resolve().parent
load_dotenv(basedir / ".env")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")

    # TEMP hardcoded Railway public DB URL
    db_url = "postgresql://postgres:UWcqpRvckrPmXxtQbzZCiKbsmPxSkJhC@viaduct.proxy.rlwy.net:20820/railway"

    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url.replace(
        "postgresql://",
        "postgresql+psycopg://"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET")

    UPLOAD_FOLDER = "uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024