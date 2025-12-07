from flask import request
from data import sessions, users

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
