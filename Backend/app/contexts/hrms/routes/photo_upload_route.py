# app/contexts/hrms/routes/photo_upload_route.py
"""
Photo upload endpoint for employee shift check-in selfies.
Handles multipart/form-data uploads and stores files locally.
"""
import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from app.contexts.core.security.decorators import require_auth, require_role


photo_upload_bp = Blueprint("photo_upload", __name__)

# Configuration
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads", "attendance_photos")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@photo_upload_bp.route("/api/uploads/photo", methods=["POST"])
@require_auth
@require_role("employee", "manager", "hr_admin")
def upload_photo():
    """
    Upload employee shift photo (selfie).
    
    Request:
        - Content-Type: multipart/form-data
        - Field: photo (file)
        - Optional: employee_id (string)
    
    Response:
        {
            "success": true,
            "photo_url": "/uploads/attendance_photos/2026-02-13_abc123.jpg",
            "filename": "2026-02-13_abc123.jpg"
        }
    """
    try:
        # Check if file is in request
        if "photo" not in request.files:
            return jsonify({
                "success": False,
                "error": "No photo file provided"
            }), 400
        
        file = request.files["photo"]
        
        # Check if file is selected
        if file.filename == "":
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                "success": False,
                "error": f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # Check file size (if possible)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                "success": False,
                "error": f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024:.0f}MB"
            }), 400
        
        # Generate unique filename
        timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        unique_id = str(uuid.uuid4())[:8]
        extension = file.filename.rsplit(".", 1)[1].lower()
        filename = f"{timestamp}_{unique_id}.{extension}"
        filename = secure_filename(filename)
        
        # Save file
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Generate URL (relative path for serving)
        photo_url = f"/uploads/attendance_photos/{filename}"
        
        return jsonify({
            "success": True,
            "photo_url": photo_url,
            "filename": filename,
            "size_bytes": file_size
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Upload failed: {str(e)}"
        }), 500


@photo_upload_bp.route("/uploads/attendance_photos/<filename>", methods=["GET"])
def serve_photo(filename: str):
    """
    Serve uploaded attendance photos.
    This is a simple implementation - in production, use nginx or CDN.
    """
    from flask import send_from_directory
    
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        return jsonify({"error": "Photo not found"}), 404
