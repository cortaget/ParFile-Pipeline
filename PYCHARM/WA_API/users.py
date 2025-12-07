from flask import Blueprint, request, jsonify
from data import users, user_counter, submissions
from auth import get_current_user

users_bp = Blueprint('users', __name__, url_prefix='/restapi/v1')


# curl -X POST http://127.0.0.1:80/restapi/v1/users -H "Content-Type: application/json" -d "{\"name\": \"Martin\",\"email\":\"pepa@gmail.com\" ,\"role\": \"soutezici\", \"password\": \"123\"}"
@users_bp.route('/users', methods=['POST'])
def register_user():
    from data import user_counter
    import data

    req_data = request.get_json()

    user = {
        "id": data.user_counter,
        "name": req_data["name"],
        "email": req_data["email"],
        "role": req_data["role"],
        "password": req_data["password"]
    }

    users[data.user_counter] = user
    data.user_counter += 1
    return jsonify(user), 201


# curl -X GET http://127.0.0.1:80/restapi/v1/users
@users_bp.route('/users', methods=['GET'])
def get_all_users():
    return jsonify(list(users.values())), 200


# curl -X GET http://127.0.0.1:80/restapi/v1/me -H "Authorization: Bearer <token>"
@users_bp.route('/me', methods=['GET'])
def get_current_user_info():
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized — provide valid Bearer token"}), 401

    user_info = {
        "id": current_user["id"],
        "name": current_user["name"],
        "email": current_user["email"],
        "role": current_user["role"]
    }

    user_submissions = [sub for sub in submissions.values() if sub["user_id"] == current_user["id"]]
    user_info["submissions"] = user_submissions

    return jsonify(user_info), 200