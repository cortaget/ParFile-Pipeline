from flask import Blueprint, request, jsonify
from data import results, rounds, participants, submissions, ratings
from auth import get_current_user

results_bp = Blueprint('results', __name__, url_prefix='/restapi/v1')

# curl -X GET http://127.0.0.1:80/restapi/v1/rounds/1/results -H "Authorization: Bearer <token>"
@results_bp.route('/rounds/<int:round_id>/results', methods=['GET'])
def calculate_results(round_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized — provide valid Bearer token"}), 401

    if round_id not in rounds:
        return jsonify({"error": "Round not found"}), 404

    participant_list = participants.get(round_id, [])
    if not participant_list:
        return jsonify({"error": "No participants in this round"}), 404

    round_results = []
    for p in participant_list:
        user_subs = [sub for sub in submissions.values() if sub["user_id"] == p["user_id"]]
        total_points = 0
        count_points = 0
        for sub in user_subs:
            sub_ratings = ratings.get(sub["id"], [])
            for r in sub_ratings:
                total_points += r["points"]
                count_points += 1

        avg_points = total_points / count_points if count_points > 0 else 0
        round_results.append({
            "user_id": p["user_id"],
            "score": avg_points
        })

    round_results.sort(key=lambda x: x["score"], reverse=True)
    for idx, r in enumerate(round_results, start=1):
        r["rank"] = idx

    results[round_id] = round_results
    return jsonify(round_results), 200

# curl -X POST http://127.0.0.1:80/restapi/v1/rounds/1/publish -H "Authorization: Bearer <token>"
@results_bp.route('/rounds/<int:round_id>/publish', methods=['POST'])
def publish_results(round_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized — provide valid Bearer token"}), 401

    if current_user["role"] != "poradatel":
        return jsonify({"error": "Only poradatel can publish results"}), 403

    if round_id not in results:
        return jsonify({"error": "No results calculated yet"}), 400

    rounds[round_id]["published"] = True
    return jsonify({"message": f"Results for round {round_id} have been published"}), 200

# curl -X GET http://127.0.0.1:80/restapi/v1/public/results
@results_bp.route('/public/results', methods=['GET'])
def public_results():
    public_list = []
    for round_id, round_info in rounds.items():
        if round_info.get("published"):
            public_list.append({
                "round_id": round_id,
                "name": round_info["name"],
                "results": results.get(round_id, [])
            })
    return jsonify(public_list), 200