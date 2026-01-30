def build_event(payload):
    return {
        "request_id": payload["request_id"],
        "author": payload["author"],
        "action": payload["action"],
        "from_branch": payload.get("from_branch"),
        "to_branch": payload.get("to_branch"),
        "timestamp": payload["timestamp"]
    }
