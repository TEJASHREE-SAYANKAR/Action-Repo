from flask import Flask
from routes.webhook import webhook_bp
from routes.events import events_bp

app = Flask(__name__)

app.register_blueprint(webhook_bp)
app.register_blueprint(events_bp)

@app.route("/")
def health():
    return "Webhook server is running"


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
