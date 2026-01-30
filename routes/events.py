from flask import Blueprint, jsonify
from database.mongo import collection

events_bp = Blueprint("events", __name__)

@events_bp.route("/events", methods=["GET"])
def get_events():
    data = list(
        collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(20)
    )
    return jsonify(data)
