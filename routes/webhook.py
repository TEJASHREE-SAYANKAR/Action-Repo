from flask import Blueprint, request, jsonify
from services.github_parser import parse_github_event
from database.mongo import collection

webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.route("/webhook", methods=["POST"])
def github_webhook():
    print("Webhook received!") 

    event = parse_github_event(request.headers, request.json)

    if not event:
        print("Ignored event")
        return jsonify({"message": "Ignored event"}), 200

    collection.insert_one(event)
    print("Event stored:", event)   

    return jsonify({"status": "stored"}), 201
