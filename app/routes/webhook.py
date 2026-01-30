from flask import Blueprint, request, jsonify
from app.db import db
import uuid
from datetime import datetime

webhook_bp = Blueprint("webhook", __name__)


def format_timestamp(ts):
    if not ts:
        return None
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return dt.strftime("%d %B %Y - %I:%M %p UTC")


@webhook_bp.route("/webhook/github", methods=["POST"])
def github_webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    try:
        # ---------------- PUSH ----------------
        if event_type == "push":
            author = payload.get("pusher", {}).get("name", "Unknown")
            ref = payload.get("ref", "")
            to_branch = ref.split("/")[-1] if ref else "unknown"
            timestamp = format_timestamp(
                payload.get("head_commit", {}).get("timestamp")
            )

            event_data = {
                "request_id": str(uuid.uuid4()),
                "author": author,
                "action": "PUSH",
                "from_branch": "",
                "to_branch": to_branch,
                "timestamp": timestamp
            }

            db.events.insert_one(event_data)
            return jsonify({"message": "Push event stored"}), 200

        # ------------- PULL REQUEST / MERGE -------------
        if event_type == "pull_request":
            action = payload.get("action")
            pr = payload.get("pull_request", {})

            author = pr.get("user", {}).get("login", "Unknown")
            from_branch = pr.get("head", {}).get("ref", "")
            to_branch = pr.get("base", {}).get("ref", "")
            timestamp = format_timestamp(pr.get("created_at"))

            # ---- PULL REQUEST OPENED ----
            if action == "opened":
                event_action = "PULL"

            # ---- MERGE ----
            elif action == "closed" and pr.get("merged") is True:
                event_action = "MERGE"
                timestamp = format_timestamp(pr.get("merged_at"))

            else:
                return jsonify({"message": "PR event ignored"}), 200

            event_data = {
                "request_id": str(uuid.uuid4()),
                "author": author,
                "action": event_action,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }

            db.events.insert_one(event_data)
            return jsonify({"message": f"{event_action} event stored"}), 200

        return jsonify({"message": "Event not handled"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
