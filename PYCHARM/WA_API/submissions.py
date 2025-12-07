from flask import Blueprint, request, jsonify
from data import submissions, counter_submissions
from auth import get_current_user

submissions_bp = Blueprint('submissions', __name__, url_prefix='/restapi/v1')


# curl -X POST http://127.0.0.1:80/restapi/v1/submissions -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d "{\"name\":\"Hack\"}"
@submissions_bp.route('/submissions', methods=['POST'])
def create_submission():
    import data

    req_data = request.get_json()
    if not req_data or "name" not in req_data:
        return jsonify({"error": "Missing 'name'"}), 400

    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized — provide valid Bearer token"}), 401

    if current_user.get("role") != "soutezici":
        return jsonify({"error": "Only soutezici can create submissions"}), 403

    submission = {
        "id": data.counter_submissions,
        "name": req_data["name"],
        "user_id": current_user["id"]
    }

    submissions[data.counter_submissions] = submission
    data.counter_submissions += 1
    return jsonify(submission), 201


# curl -X GET http://127.0.0.1:80/restapi/v1/submissions
@submissions_bp.route('/submissions', methods=['GET'])
def get_all_submissions():
    return jsonify(list(submissions.values())), 200


# curl -X PUT http://127.0.0.1:80/restapi/v1/submissions/1 -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d "{\"name\":\"Updated\"}"
@submissions_bp.route('/submissions/<int:sub_id>', methods=['PUT'])
def update_submission(sub_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized — provide valid Bearer token"}), 401

    if current_user.get("role") != "soutezici":
        return jsonify({"error": "Only soutezici can update submissions"}), 403

    submission = submissions.get(sub_id)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404

    if submission["user_id"] != current_user["id"]:
        return jsonify({"error": "You can edit only your own submission"}), 403

    req_data = request.get_json()
    if not req_data:
        return jsonify({"error": "No data provided"}), 400

    if "name" in req_data:
        submission["name"] = req_data["name"]

    return jsonify(submission), 200


# curl -X DELETE http://127.0.0.1:80/restapi/v1/submissions/1 -H "Authorization: Bearer <token>"
@submissions_bp.route('/submissions/<int:sub_id>', methods=['DELETE'])
def delete_submission(sub_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized — provide valid Bearer token"}), 401

    submission = submissions.get(sub_id)
    if not submission:
        return jsonify({"error": f"Submission {sub_id} not found"}), 404

    if submission["user_id"] != current_user["id"]:
        return jsonify({"error": "You can delete only your own submission"}), 403

    del submissions[sub_id]
    return jsonify({"message": f"Submission {sub_id} deleted"}), 200