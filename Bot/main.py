# main.py
import os
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

slack_token = os.getenv("SLACK_BOT_TOKEN")
signing_secret = os.getenv("SLACK_SIGNING_SECRET")

client = WebClient(token=slack_token)
verifier = SignatureVerifier(signing_secret=signing_secret) # type: ignore

@app.route("/slack/events", methods=["POST"])
def slack_events():
    # Verify request signature
    if not verifier.is_valid_request(request.get_data(), dict(request.headers)):
        return "Invalid request", 403

    data = request.json

    # Slack URL verification challenge
    if "challenge" in data: # type: ignore
        return jsonify({"challenge": data["challenge"]}) # type: ignore

    # Handle app_mention events
    if "event" in data: # type: ignore
        event = data["event"] # type: ignore

        if event.get("type") == "app_mention":
            channel = event.get("channel")
            user = event.get("user")
            text = event.get("text")

            # Send a reply
            client.chat_postMessage(
                channel=channel,
                text=f"Hi <@{user}>! 👋 You said: {text}"
            )

    return "", 200


if __name__ == "__main__":
    app.run(port=3000)
