import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI, Request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests

load_dotenv()

# Load API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_REDIRECT_URI = os.getenv("SLACK_REDIRECT_URI")
SLACK_CLIENT_ID = os.getenv("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET")


# Initialize Slack Client
client = WebClient(token=SLACK_BOT_TOKEN)

# Initialize Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-8b")

app = FastAPI()

# Store message history per channel
message_history = {}

@app.post("/slack/events")
async def slack_events(request: Request):
    data = await request.json()

    # Slack Verification Challenge
    if "challenge" in data:
        return {"challenge": data["challenge"]}

    if data.get("event"):
        event = data["event"]
        channel_id = event.get("channel")
        user_message = event.get("text")
        bot_id = event.get("bot_id")

        # Ignore bot messages
        if bot_id:
            return {"status": "Bot message ignored"}

        # Store last 5 messages for context
        if channel_id not in message_history:
            message_history[channel_id] = []
        message_history[channel_id].append(user_message)
        message_history[channel_id] = message_history[channel_id][-5:]  # Keep last 5

        # Generate AI response
        history = "\n".join(message_history[channel_id])
        prompt = f"Conversation history:\n{history}\n\nNew user message: {user_message}\n\nRespond in a helpful way."
        response = model.generate_content([prompt])
        bot_reply = response.text if response else "I couldn't generate a response."

        # Send response to Slack
        try:
            client.chat_postMessage(channel=channel_id, text=bot_reply)
        except SlackApiError as e:
            print(f"Error posting message: {e.response['error']}")

    return {"status": "ok"}


@app.get("/slack/oauth")
async def slack_oauth(request: Request):
    """Handle OAuth callback and install bot in workspace"""
    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing code"}

    # Exchange code for access token
    response = requests.post("https://slack.com/api/oauth.v2.access", data={
        "client_id": SLACK_CLIENT_ID,
        "client_secret": SLACK_CLIENT_SECRET,
        "code": code,
        "redirect_uri": SLACK_REDIRECT_URI
    }).json()

    if not response.get("ok"):
        return {"error": "OAuth failed", "details": response}

    bot_token = response["access_token"]
    workspace = response["team"]["name"]

    return {"message": f"Bot successfully installed in {workspace}!", "token": bot_token}