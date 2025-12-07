from flask import Blueprint, request, jsonify
from data import participants, rounds
from auth import get_current_user

participants_bp = Blueprint('participants', __name__, url_prefix='/restapi/v1')

# curl -X POST http://127.0.0.1:80/restapi/v1/rounds/1/participants -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d "{\"user_id\": 2, \"status\":\"active\"}"
@participants_bp.route('/rounds/<int:round_id>/participants', methods=['POST'])
def add_participant(round_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized — provide valid Bearer token"}), 401

    if current_user["role"] != "poradatel":
        return jsonify({"error": "Only poradatel can manage participants"}), 403

    if round_id not in rounds:
        return jsonify({"error": "Round not found"}), 404

    req_data = request.get_json()
    if not req_data or "user_id" not in req_data or "status" not in req_data:
        return jsonify({"error": "Missing 'user_id' or 'status'"}), 400

    participant_list = participants.setdefault(round_id, [])
    for p in participant_list:
        if p["user_id"] == req_data["user_id"]:
            return jsonify({"error": "User already in participants"}), 400

    new_participant = {
        "user_id": req_data["user_id"],
        "status": req_data["status"]
    }
    participant_list.append(new_participant)
    return jsonify(new_participant), 201

# curl -X GET http://127.0.0.1:80/restapi/v1/rounds/1/participants
@participants_bp.route('/rounds/<int:round_id>/participants', methods=['GET'])
def get_participants(round_id):
    if round_id not in rounds:
        return jsonify({"error": "Round not found"}), 404

    participant_list = participants.get(round_id, [])
    return jsonify(participant_list), 200

# curl -X PUT http://127.0.0.1:80/restapi/v1/rounds/1/participants/2 -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d "{\"status\":\"inactive\"}"
@participants_bp.route('/rounds/<int:round_id>/participants/<int:user_id>', methods=['PUT'])
def update_participant(round_id, user_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized — provide valid Bearer token"}), 401

    if current_user["role"] != "poradatel":
        return jsonify({"error": "Only poradatel can update participants"}), 403

    participant_list = participants.get(round_id)
    if not participant_list:
        return jsonify({"error": "Round has no participants"}), 404

    for p in participant_list:
        if p["user_id"] == user_id:
            req_data = request.get_json()
            if not req_data or "status" not in req_data:
                return jsonify({"error": "Missing 'status'"}), 400
            p["status"] = req_data["status"]
            return jsonify(p), 200

    return jsonify({"error": "Participant not found"}), 404

# curl -X DELETE http://127.0.0.1:80/restapi/v1/rounds/1/participants/2 -H "Authorization: Bearer <token>"
@participants_bp.route('/rounds/<int:round_id>/participants/<int:user_id>', methods=['DELETE'])
def delete_participant(round_id, user_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized — provide valid Bearer token"}), 401

    if current_user["role"] != "poradatel":
        return jsonify({"error": "Only poradatel can delete participants"}), 403

    participant_list = participants.get(round_id)
    if not participant_list:
        return jsonify({"error": "Round has no participants"}), 404

    for p in participant_list:
        if p["user_id"] == user_id:
            participant_list.remove(p)
            return jsonify({"message": f"Participant {user_id} removed from round {round_id}"}), 200

    return jsonify({"error": "Participant not found"}), 404