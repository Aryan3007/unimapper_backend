from flask import Blueprint, request, jsonify
from .models import (
    create_note,
    get_note,
    update_note,
    delete_note,
    get_all_notes,
    get_notes_by_user,
)
from .utils import token_required

note_bp = Blueprint("notes", __name__)


# Create a Note
@note_bp.route("/", methods=["POST"])
@token_required
def create_note_route():
    data = request.json
    name = data.get("name", "").strip()
    description = data.get("description", "").strip()
    content = data.get("content", "").strip()
    flowchart_id = data.get("flowchart_id", None)
    user_id = request.user_id

    if not name or not description or not content:
        return jsonify({"message": "Name, description, and content are required"}), 400

    try:
        create_note(name, description, content, user_id, flowchart_id)
        return jsonify({"message": "Note created successfully"}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


# Read a Note
@note_bp.route("/<note_id>", methods=["GET"])
@token_required
def get_note_route(note_id):
    note = get_note(note_id)
    if note:
        return jsonify(note), 200
    return jsonify({"message": "Note not found"}), 404


# Update a Note
@note_bp.route("/<note_id>", methods=["PUT"])
@token_required
def update_note_route(note_id):
    data = request.json
    update_fields = {}
    if "name" in data:
        update_fields["name"] = data["name"].strip()
    if "description" in data:
        update_fields["description"] = data["description"].strip()
    if "content" in data:
        update_fields["content"] = data["content"].strip()
    if "flowchart_id" in data:
        update_fields["flowchart_id"] = data["flowchart_id"].strip()

    if update_note(note_id, update_fields):
        return jsonify({"message": "Note updated successfully"}), 200
    return jsonify({"message": "Note not found or no changes made"}), 404


# Delete a Note
@note_bp.route("/<note_id>", methods=["DELETE"])
@token_required
def delete_note_route(note_id):
    if delete_note(note_id):
        return jsonify({"message": "Note deleted successfully"}), 200
    return jsonify({"message": "Note not found"}), 404


# Get All Notes
@note_bp.route("/", methods=["GET"])
@token_required
def get_all_notes_route():
    user_id = request.user_id
    notes = get_notes_by_user(user_id)
    return jsonify(notes), 200


# Get All Notes by User ID
@note_bp.route("/user/<user_id>", methods=["GET"])
@token_required
def get_notes_by_user_route(user_id):
    notes = get_notes_by_user(user_id)
    return jsonify(notes), 200
