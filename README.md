# Slack Chatbot with FastAPI

## Introduction
This project is a Slack chatbot that listens for mentions in a Slack channel, fetches the last 5 messages (including bot responses), sends them to OpenAI's API for a response, and replies in the same thread. The bot is built using FastAPI and integrates with Slack and OpenAI.

## Features
- Listens to messages where the bot is mentioned.
- Stores past messages in a SQLite database.
- Sends the last 5 messages (user and bot) to OpenAI's API for better contextual responses.
- Replies in Slack using Slack API.

## Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** SQLite
- **APIs:** OpenAI API, Slack API
- **Deployment:** Docker (Optional), Ngrok for local testing

## Installation & Setup

### Prerequisites
1. Python 3.8+
2. Slack App with Bot Token
3. OpenAI API Key
4. Ngrok (for local testing)

### Environment Variables
Create a `.env` file in the root directory and add:
```
SLACK_BOT_TOKEN=your-slack-bot-token
SLACK_SIGNING_SECRET=your-slack-signing-secret
OPENAI_API_KEY=your-openai-api-key
```

### Install Dependencies
```
pip install -r requirements.txt
```

### Database Setup
```
python setup_db.py
```

### Run Locally
```
uvicorn main:app --reload
```

Expose the FastAPI server to Slack using Ngrok:
```
ngrok http 8000
```
Update the Slack event URL with the generated Ngrok URL.

## Slack Bot Setup
1. Create a Slack App at [Slack API](https://api.slack.com/apps)
2. Enable **Bot Token Scopes**: `chat:write`, `channels:history`, `commands`
3. Add your bot to a Slack channel
4. Set up event subscriptions pointing to `/slack/events`

## Usage
Mention the bot in a Slack channel:
```
@YourBotName How do I deploy this?
```
The bot will fetch the conversation history, send it to OpenAI, and reply with a relevant response.

## Deployment
Use Docker or cloud services (AWS, GCP, Heroku) to deploy the bot.

### Docker Deployment
```
docker build -t slack-chatbot .
docker run -p 8000:8000 --env-file .env slack-chatbot
```

## Contributing
Feel free to fork this repository and submit a PR with improvements.

## License
This project is licensed under the MIT License.

