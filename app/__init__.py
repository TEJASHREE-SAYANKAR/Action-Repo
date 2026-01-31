from flask import Flask
from dotenv import load_dotenv
from app.db import init_db

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Initialize MongoDB
    init_db()

    # Register blueprints
    from app.routes.webhook import webhook_bp
    from app.routes.ui import ui_bp

    app.register_blueprint(webhook_bp)
    app.register_blueprint(ui_bp)

    return app




