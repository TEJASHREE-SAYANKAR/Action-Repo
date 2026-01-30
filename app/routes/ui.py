from flask import Blueprint, jsonify, render_template
from app.db import db

ui_bp = Blueprint("ui", __name__)


@ui_bp.route("/")
def index():
    return render_template("index.html")


@ui_bp.route("/events")
def get_events():
    events = db.events.find().sort("_id", -1).limit(20)

    response = []
    for event in events:
        response.append({
            "author": event.get("author"),
            "action": event.get("action"),
            "from_branch": event.get("from_branch"),
            "to_branch": event.get("to_branch"),
            "timestamp": event.get("timestamp")
        })

    return jsonify(response)
