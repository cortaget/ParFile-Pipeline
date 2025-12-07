from flask import Blueprint, request, jsonify
from data import reports, rounds, participants, results
from auth import get_current_user

reports_bp = Blueprint('reports', __name__, url_prefix='/restapi/v1')

# curl -X GET http://127.0.0.1:80/restapi/v1/rounds/1/report?format=pdf -H "Authorization: Bearer <token>"
@reports_bp.route('/rounds/<int:round_id>/report', methods=['GET'])
def generate_report(round_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized — provide valid Bearer token"}), 401

    if current_user["role"] not in ["poradatel", "admin"]:
        return jsonify({"error": "Only poradatel or admin can generate reports"}), 403

    if round_id not in rounds:
        return jsonify({"error": "Round not found"}), 404

    report_format = request.args.get("format", "pdf").lower()
    participant_list = participants.get(round_id, [])
    round_results = results.get(round_id, [])

    report_content = f"Report for round {rounds[round_id]['name']}\n\nParticipants:\n"
    for p in participant_list:
        report_content += f"User ID: {p['user_id']}, Status: {p['status']}\n"

    report_content += "\nResults:\n"
    for r in round_results:
        report_content += f"User ID: {r['user_id']}, Score: {r['score']}, Rank: {r['rank']}\n"

    reports[round_id] = report_content

    return jsonify({
        "round_id": round_id,
        "format": report_format,
        "report": report_content,
        "message": f"This is a mock {report_format.upper()} report"
    }), 200