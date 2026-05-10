from pathlib import Path
from uuid import uuid4

import cloudinary.uploader
from flask import current_app, url_for
from werkzeug.utils import secure_filename


def _cloudinary_is_configured():
    cloud_name = current_app.config.get("CLOUDINARY_CLOUD_NAME")
    api_key = current_app.config.get("CLOUDINARY_API_KEY")
    api_secret = current_app.config.get("CLOUDINARY_API_SECRET")
    values = [cloud_name, api_key, api_secret]
    return all(values) and all(not str(v).startswith("your_") for v in values)


def upload_image_file(file_obj, folder="uniswap/listings"):
    if file_obj is None:
        return {}

    if _cloudinary_is_configured():
        try:
            return cloudinary.uploader.upload(
                file_obj,
                folder=folder,
                overwrite=True,
                resource_type="image",
            )
        except Exception:
            pass

    # Fallback for local development when Cloudinary is not configured.
    upload_dir = Path(current_app.static_folder) / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    original = secure_filename(getattr(file_obj, "filename", "") or "upload")
    ext = Path(original).suffix.lower() or ".jpg"
    filename = f"{uuid4().hex}{ext}"
    file_obj.save(upload_dir / filename)
    return {"secure_url": url_for("static", filename=f"uploads/{filename}")}
