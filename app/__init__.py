from flask import Flask
from dotenv import load_dotenv
from app.db import init_db
from app.routes.ui import ui_bp

load_dotenv()

def create_app():
   
    app = Flask(__name__)
    app.register_blueprint(ui_bp)

    # Initialize MongoDB
    init_db()

    # Import blueprints INSIDE function (important!)
    from app.routes.webhook import webhook_bp
    app.register_blueprint(webhook_bp)

    @app.route("/")
    def health():
        return {"status": "OK", "message": "Flask app is running"}

    return app
