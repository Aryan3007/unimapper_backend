from flask import Blueprint, request, jsonify
from .utils import token_required

from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
from .models import create_flowchart, read_flowchart, update_flowchart, delete_flowchart

flowcharts_bp = Blueprint('flowcharts', __name__)

@flowcharts_bp.route('/', methods=['POST'])
@token_required
def create_flowchart_route():
    data = request.json
    if not data:
        raise BadRequest("No data provided")

    edges = data.get("edges")
    nodes = data.get("nodes")
    title = data.get("title")

    if not edges or not nodes or not title:
        raise BadRequest("Missing required fields")

    flowchart_id = create_flowchart(edges, nodes, title)
    return jsonify({"id": str(flowchart_id)}), 201

@flowcharts_bp.route('/<flowchart_id>', methods=['GET'])
@token_required
def read_flowchart_route(flowchart_id):
    flowchart = read_flowchart(flowchart_id)
    if not flowchart:
        raise NotFound("Flowchart not found")

    flowchart["_id"] = str(flowchart["_id"])
    return jsonify(flowchart), 200

@flowcharts_bp.route('/<flowchart_id>', methods=['PUT'])
@token_required
def update_flowchart_route(flowchart_id):
    data = request.json
    if not data:
        raise BadRequest("No data provided")

    update_fields = {}
    if "edges" in data:
        update_fields["edges"] = data["edges"]
    if "nodes" in data:
        update_fields["nodes"] = data["nodes"]
    if "title" in data:
        update_fields["title"] = data["title"]

    if not update_fields:
        raise BadRequest("No fields to update")

    modified_count = update_flowchart(flowchart_id, **update_fields)

    return jsonify({"modified_count": modified_count}), 200

@flowcharts_bp.route('/<flowchart_id>', methods=['DELETE'])
@token_required
def delete_flowchart_route(flowchart_id):
    deleted_count = delete_flowchart(flowchart_id)
    if deleted_count == 0:
        raise NotFound("Flowchart not found")

    return jsonify({"deleted_count": deleted_count}), 200
