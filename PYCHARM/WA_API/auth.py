from flask import Blueprint, request, jsonify
import uuid
from data import users, sessions

auth_bp = Blueprint('auth', __name__, url_prefix='/restapi/v1')

def get_current_user():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth.split(" ", 1)[1].strip()
    user_id = sessions.get(token)
    if not user_id:
        return None
    user = users.get(user_id)
    if not user:
        return None
    return user

# curl -X POST http://127.0.0.1:80/restapi/v1/login -H "Content-Type: application/json" -d "{\"name\": \"Martin\",\"password\": \"123\"}"
@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name'"}), 400

    # поиск пользователя по имени
    found_user = None
    for u in users.values():
        if u["name"] == data["name"]:
            found_user = u
            break

    if not found_user:
        return jsonify({"error": "User not found"}), 404
    if found_user["password"] != data["password"]:
        return jsonify({"error": "Incorrect password"}), 403

    # создаём токен сессии
    token = str(uuid.uuid4())
    sessions[token] = found_user["id"]
    return jsonify({"message": "Logged in", "token": token}), 200

# curl -X POST http://127.0.0.1:80/restapi/v1/logout -H "Authorization: Bearer <token>"
@auth_bp.route('/logout', methods=['POST'])
def logout():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "Missing token"}), 400
    token = auth.split(" ", 1)[1].strip()
    sessions.pop(token, None)
    return jsonify({"message": "Logged out"}), 200