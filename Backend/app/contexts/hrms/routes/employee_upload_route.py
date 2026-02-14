import os
from urllib.parse import urlparse
from app.contexts.shared.model_converter import mongo_converter
from app.contexts.hrms.data_transfer.response.employee_response import EmployeeDTO
from flask import Blueprint, request, jsonify, send_from_directory, g
from werkzeug.utils import secure_filename

employee_upload_bp = Blueprint("employee_upload_bp", __name__, url_prefix="/uploads")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
UPLOAD_ROOT = os.path.join(PROJECT_ROOT, "backend", "uploads")
os.makedirs(UPLOAD_ROOT, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, entity_folder: str, entity_id: str) -> str:
    if not file or not allowed_file(file.filename):
        raise ValueError("Invalid or missing file")

    folder = os.path.join(UPLOAD_ROOT, entity_folder)
    os.makedirs(folder, exist_ok=True)

    ext = os.path.splitext(secure_filename(file.filename))[1].lower()
    filename = f"{entity_id}{ext}"
    filepath = os.path.join(folder, filename)
    file.save(filepath)

    # Return full URL
    return f"{request.host_url.rstrip('/')}/uploads/{entity_folder}/{filename}"


def delete_file(file_url: str):
    """Works with full URL like https://domain/uploads/employees/<id>.jpg"""
    if not file_url:
        return

    parsed = urlparse(file_url)
    path = parsed.path  # /uploads/employees/<filename>
    parts = [p for p in path.split("/") if p]

    # expected: ["uploads", "<entity_folder>", "<filename>"]
    if len(parts) < 3 or parts[0] != "uploads":
        return

    entity_folder = parts[1]
    filename = parts[2]

    filepath = os.path.join(UPLOAD_ROOT, entity_folder, filename)
    if os.path.exists(filepath):
        os.remove(filepath)


# === Serve uploaded files (GET /uploads/<entity_folder>/<filename>) ===
@employee_upload_bp.route("/<entity_folder>/<filename>", methods=["GET"])
def serve_file(entity_folder, filename):
    folder_path = os.path.join(UPLOAD_ROOT, entity_folder)
    return send_from_directory(folder_path, filename)


@employee_upload_bp.route("/employee/<employee_id>", methods=["PATCH"])
def upload_employee_photo(employee_id: str):
    try:
        file = request.files.get("photo")
        if not file:
            return jsonify({"success": False, "message": "No file uploaded"}), 400

        old_photo_url = request.form.get("old_photo_url")
        if old_photo_url:
            delete_file(old_photo_url)

        photo_url = save_file(file, "employees", employee_id)
        emp = g.hrms.employee_service.set_employee_photo(employee_id, photo_url=photo_url)  # domain Employee

        emp_dict = g.hrms.employee_service._mapper.to_persistence(emp)  # dict
        employee_dto = mongo_converter.doc_to_dto(emp_dict, EmployeeDTO)

        return jsonify({
            "success": True,
            "message": "Photo uploaded successfully",
            "photo_url": photo_url,
            "employee": employee_dto.model_dump() if hasattr(employee_dto, "model_dump") else employee_dto
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500