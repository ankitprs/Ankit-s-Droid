import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI, Request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
from gemini_api import generate_gemini_response 

load_dotenv()

# Load API Keys
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_REDIRECT_URI = os.getenv("SLACK_REDIRECT_URI")
SLACK_CLIENT_ID = os.getenv("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET")


# Initialize Slack Client
client = WebClient(token=SLACK_BOT_TOKEN)

app = FastAPI()

# Store message history per channel
message_history = {}

# Store Access Tokens
access_tokens = {}

@app.post("/slack/events")
async def slack_events(request: Request):
    data = await request.json()
    # for debugging
    print(f"Received data: {data}")

    # Slack Verification Challenge
    if "challenge" in data:
        return {"challenge": data["challenge"]}

    if data.get("event"):
        event = data["event"]
        channel_id = event.get("channel")
        user_message = event.get("text")
        bot_id = event.get("bot_id")
        team_id = data.get("team_id")

        # Ignore bot messages
        if bot_id:
            return {"status": "Bot message ignored"}

        # Store last 5 messages for context
        if channel_id not in message_history:
            message_history[channel_id] = []
        message_history[channel_id].append({"role": "user", "parts": [user_message]})
        message_history[channel_id] = message_history[channel_id][-5:]  # Keep last 5

        # Generate AI response
        history = message_history[channel_id]
        bot_reply = generate_gemini_response(history)
        message_history[channel_id].append({"role": "model", "parts": [bot_reply]})

        # Initialize Slack Client & send message
        try:
            ACCESS_TOKEN = access_tokens[team_id]
            client = WebClient(token=ACCESS_TOKEN)
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
    
    # for debugging
    print(f"Received OAuth response: {response}")

    if not response.get("ok"):
        return {"error": "OAuth failed", "details": response}

    bot_token = response["access_token"]
    workspace = response["team"]["name"]
    access_tokens[response["team"]["id"]] = bot_token

    return {"message": f"Bot successfully installed in {workspace}!", "token": bot_token}