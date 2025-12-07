from flask import Blueprint, request, jsonify
from data import ratings, submissions, participants
from auth import get_current_user

ratings_bp = Blueprint('ratings', __name__, url_prefix='/restapi/v1')

# curl -X POST http://127.0.0.1:80/restapi/v1/submissions/1/ratings -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d "{\"points\":85, \"comment\":\"Výborná práce\"}"
@ratings_bp.route('/submissions/<int:submission_id>/ratings', methods=['POST'])
def rate_submission(submission_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized — provide valid Bearer token"}), 401

    if current_user["role"] != "porotce":
        return jsonify({"error": "Only porotce can rate submissions"}), 403

    submission = submissions.get(submission_id)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404

    req_data = request.get_json()
    if not req_data or "points" not in req_data or "comment" not in req_data:
        return jsonify({"error": "Missing 'points' or 'comment'"}), 400

    rating = {
        "points": req_data["points"],
        "comment": req_data["comment"],
        "judge_id": current_user["id"]
    }

    ratings.setdefault(submission_id, []).append(rating)
    return jsonify(rating), 201

# curl -X GET http://127.0.0.1:80/restapi/v1/submissions/1/ratings
@ratings_bp.route('/submissions/<int:submission_id>/ratings', methods=['GET'])
def get_ratings(submission_id):
    submission = submissions.get(submission_id)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404

    submission_ratings = ratings.get(submission_id, [])
    return jsonify(submission_ratings), 200

# curl -X GET http://127.0.0.1:80/restapi/v1/rounds/1/submissions/pdf -H "Authorization: Bearer <token>"
@ratings_bp.route('/rounds/<int:round_id>/submissions/pdf', methods=['GET'])
def download_submissions_pdf(round_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized — provide valid Bearer token"}), 401

    if current_user["role"] != "porotce":
        return jsonify({"error": "Only porotce can download submissions PDF"}), 403

    participant_list = participants.get(round_id, [])
    submission_list = [sub for sub in submissions.values() if any(p["user_id"] == sub["user_id"] for p in participant_list)]

    pdf_content = "PDF obsah soutěžních prací:\n\n"
    for sub in submission_list:
        pdf_content += f"ID: {sub['id']}, Name: {sub['name']}, User: {sub['user_id']}\n"

    return jsonify({"pdf": pdf_content, "message": "This is a mock PDF content"}), 200