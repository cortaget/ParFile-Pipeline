from flask import Flask
from auth import auth_bp
from users import users_bp
from submissions import submissions_bp
from rounds import rounds_bp
from participant import participants_bp
from ratings import ratings_bp
from results import results_bp
from reports import reports_bp

app = Flask(__name__)

# Регистрация blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(submissions_bp)
app.register_blueprint(rounds_bp)
app.register_blueprint(participants_bp)
app.register_blueprint(ratings_bp)
app.register_blueprint(results_bp)
app.register_blueprint(reports_bp)

@app.route('/')
def index():
    return 'Vitejte na serveru SOC'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)