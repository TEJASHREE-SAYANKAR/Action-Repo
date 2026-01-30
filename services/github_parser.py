from datetime import datetime

def parse_github_event(headers, data):
    event_type = headers.get("X-GitHub-Event")

    base = {
        "request_id": data.get("repository", {}).get("id"),
        "author": data.get("sender", {}).get("login"),
        "timestamp": datetime.utcnow().isoformat()
    }

    if event_type == "push":
        base.update({
            "action": "PUSH",
            "to_branch": data["ref"].split("/")[-1]
        })

    elif event_type == "pull_request":
        pr = data["pull_request"]
        action = data["action"]

        if action == "closed" and pr.get("merged"):
            base.update({
                "action": "MERGE",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"]
            })
        else:
            base.update({
                "action": "PULL_REQUEST",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"]
            })

    else:
        return None

    return base
