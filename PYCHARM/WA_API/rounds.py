from flask import Blueprint, request, jsonify
from data import rounds, round_counter
from auth import get_current_user

rounds_bp = Blueprint('rounds', __name__, url_prefix='/restapi/v1')


# curl -X POST http://127.0.0.1:80/restapi/v1/rounds -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d "{\"name\":\"Kolo 1\",\"rules\":\"Pravidla\",\"start_date\":\"2025-10-01\",\"end_date\":\"2025-12-01\"}"
@rounds_bp.route('/rounds', methods=['POST'])
def create_round():
    import data

    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized — provide valid Bearer token"}), 401

    if current_user["role"] != "poradatel":
        return jsonify({"error": "Only poradatel can create rounds"}), 403

    req_data = request.get_json()
    required_fields = ["name", "rules", "start_date", "end_date"]
    for field in required_fields:
        if field not in req_data:
            return jsonify({"error": f"Missing field '{field}'"}), 400

    new_round = {
        "id": data.round_counter,
        "name": req_data["name"],
        "rules": req_data["rules"],
        "start_date": req_data["start_date"],
        "end_date": req_data["end_date"]
    }
    rounds[data.round_counter] = new_round
    data.round_counter += 1
    return jsonify(new_round), 201


# curl -X GET http://127.0.0.1:80/restapi/v1/rounds
@rounds_bp.route('/rounds', methods=['GET'])
def get_all_rounds():
    return jsonify(list(rounds.values())), 200


# curl -X GET http://127.0.0.1:80/restapi/v1/rounds/1
@rounds_bp.route('/rounds/<int:round_id>', methods=['GET'])
def get_round(round_id):
    rnd = rounds.get(round_id)
    if not rnd:
        return jsonify({"error": "Round not found"}), 404
    return jsonify(rnd), 200


# curl -X PUT http://127.0.0.1:80/restapi/v1/rounds/1 -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d "{\"name\":\"Updated Kolo\"}"
@rounds_bp.route('/rounds/<int:round_id>', methods=['PUT'])
def update_round(round_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized — provide valid Bearer token"}), 401

    if current_user["role"] != "poradatel":
        return jsonify({"error": "Only poradatel can update rounds"}), 403

    rnd = rounds.get(round_id)
    if not rnd:
        return jsonify({"error": "Round not found"}), 404

    req_data = request.get_json()
    for field in ["name", "rules", "start_date", "end_date"]:
        if field in req_data:
            rnd[field] = req_data[field]

    return jsonify(rnd), 200


# curl -X DELETE http://127.0.0.1:80/restapi/v1/rounds/1 -H "Authorization: Bearer <token>"
@rounds_bp.route('/rounds/<int:round_id>', methods=['DELETE'])
def delete_round(round_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized — provide valid Bearer token"}), 401

    if current_user["role"] != "poradatel":
        return jsonify({"error": "Only poradatel can delete rounds"}), 403

    if round_id not in rounds:
        return jsonify({"error": "Round not found"}), 404

    del rounds[round_id]
    return jsonify({"message": f"Round {round_id} deleted"}), 200