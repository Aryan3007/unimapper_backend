from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from .models import (
    create_project,
    get_project,
    update_project,
    delete_project,
    get_projects_by_user,
)
from .utils import token_required

project_bp = Blueprint("projects", __name__)


# Create a Project
@project_bp.route("/", methods=["POST"])
@token_required
def create_project_route():
    data = request.json
    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    description = data.get("description", "").strip()
    user_id = request.user_id

    if not title or not content or not description:
        return (
            jsonify(
                {"message": "All fields (title, content, description) are required"}
            ),
            400,
        )

    try:
        create_project(title, content, description, user_id)
        return jsonify({"message": "Project created successfully"}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


# Get All Projects by User ID
@project_bp.route("/", methods=["GET"])
@token_required
def get_projects_by_user_route():
    user_id = request.user_id
    projects = get_projects_by_user(user_id)
    return jsonify(projects), 200


# Read a Project
@project_bp.route("/<project_id>", methods=["GET"])
@token_required
def read_project_route(project_id):
    project = get_project(project_id)
    if project:
        return jsonify(project), 200
    return jsonify({"message": "Project not found"}), 404


# Update a Project
@project_bp.route("/<project_id>", methods=["PUT"])
@token_required
def update_project_route(project_id):
    data = request.json
    update_fields = {}
    if "title" in data:
        title = data["title"].strip()
        if title:
            update_fields["title"] = title
        else:
            return jsonify({"message": "Title cannot be empty"}), 400

    if "content" in data:
        content = data["content"].strip()
        if content:
            update_fields["content"] = content
        else:
            return jsonify({"message": "Content cannot be empty"}), 400

    if "description" in data:
        description = data["description"].strip()
        if description:
            update_fields["description"] = description
        else:
            return jsonify({"message": "Description cannot be empty"}), 400

    if not update_fields:
        return jsonify({"message": "No fields to update"}), 400

    if update_project(project_id, update_fields):
        return jsonify({"message": "Project updated successfully"}), 200
    return jsonify({"message": "Project not found or no changes made"}), 404


# Delete a Project
@project_bp.route("/<project_id>", methods=["DELETE"])
@token_required
def delete_project_route(project_id):
    if delete_project(project_id):
        return jsonify({"message": "Project deleted successfully"}), 200
    return jsonify({"message": "Project not found"}), 404
