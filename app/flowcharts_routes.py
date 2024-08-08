import os
import uuid

from datetime import datetime
from werkzeug.exceptions import BadRequest, NotFound
from flask import Blueprint, request, jsonify, current_app

from .utils import token_required
from .models import create_flowchart, read_flowchart, update_flowchart, delete_flowchart

flowcharts_bp = Blueprint("flowcharts", __name__)


@flowcharts_bp.route("/", methods=["POST"])
@token_required
def create_flowchart_route():
    if "title" not in request.form or "image" not in request.files:
        return jsonify({"message": "Title and image are required"}), 400

    title = request.form["title"]
    image_file = request.files["image"]

    if not title or not image_file:
        return jsonify({"message": "Title and image cannot be empty"}), 400

    file_extension = os.path.splitext(image_file.filename)[1]
    unique_filename = f"{uuid.uuid4().hex}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{file_extension}"
    file_path = os.path.join(
        current_app.config.get("UPLOAD_FOLDER_PATH"), unique_filename
    )
    image_file.save(file_path)

    image_file_url = f"/static/uploaded_images/{unique_filename}"

    try:
        flowchart_id = create_flowchart(title, image_file_url, unique_filename)
        return (
            jsonify(
                {
                    "message": "Flowchart created and image saved successfully",
                    "image_path": image_file_url,
                    "filename": unique_filename,
                    "flowchart_id": str(flowchart_id),
                }
            ),
            201,
        )
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@flowcharts_bp.route("/<flowchart_id>", methods=["GET"])
@token_required
def read_flowchart_route(flowchart_id):
    flowchart = read_flowchart(flowchart_id)
    if not flowchart:
        raise NotFound("Flowchart not found")

    flowchart["_id"] = str(flowchart["_id"])
    return jsonify(flowchart), 200


@flowcharts_bp.route("/<flowchart_id>", methods=["PUT"])
@token_required
def update_flowchart_route(flowchart_id):
    update_fields = {}

    title = request.form.get("title")
    if title:
        update_fields["title"] = title.strip()

    image_file = request.files.get("image")
    if image_file:
        if image_file.filename == "":
            return jsonify({"message": "No selected file"}), 400

        file_extension = os.path.splitext(image_file.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{file_extension}"
        file_path = os.path.join(
            current_app.config.get("UPLOAD_FOLDER_PATH"), unique_filename
        )

        image_file.save(file_path)

        image_file_url = f"/static/uploaded_images/{unique_filename}"
        update_fields["image_file_url"] = image_file_url
        update_fields["filename"] = unique_filename

        flowchart_data = read_flowchart(flowchart_id)

        if flowchart_data:
            file_path = os.path.join(
                current_app.config.get("UPLOAD_FOLDER_PATH"),
                flowchart_data.get("filename"),
            )

            if os.path.exists(file_path):
                os.remove(file_path)

    if not update_fields:
        return jsonify({"message": "No fields to update"}), 400

    try:
        modified_count = update_flowchart(flowchart_id, update_fields)
        if modified_count > 0:
            return (
                jsonify(
                    {
                        "message": "Flowchart updated successfully",
                        "modified_count": modified_count,
                    }
                ),
                200,
            )
        return jsonify({"message": "Flowchart not found or no changes made"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@flowcharts_bp.route("/<flowchart_id>", methods=["DELETE"])
@token_required
def delete_flowchart_route(flowchart_id):

    flowchart_data = read_flowchart(flowchart_id)

    if flowchart_data:
        file_path = os.path.join(
            current_app.config.get("UPLOAD_FOLDER_PATH"), flowchart_data.get("filename")
        )

        if os.path.exists(file_path):
            os.remove(file_path)

    deleted_count = delete_flowchart(flowchart_id)

    return jsonify({"deleted_count": deleted_count}), 200
