# **Your_Name’s Droid: A Context-Aware Slack Chatbot**

> **A powerful Slack chatbot that listens to questions, sends them to an LLM (like OpenAI/Gemini), and replies with context-aware answers, including the last 5 messages (both user + bot).**

<br/>

## **Table of Contents**
1. [Project Overview](#project-overview)  
2. [Key Features](#key-features)  
3. [Architecture Diagram](#architecture-diagram)  
4. [Installation & Setup](#installation--setup)  
5. [Slack App Installation Link](#slack-app-installation-link)  
6. [Usage](#usage)  
7. [Video Demonstration](#video-demonstration)  
8. [Repository Structure](#repository-structure)  
9. [How It Works](#how-it-works)  
10. [Future Improvements](#future-improvements)  
11. [Contributing](#contributing)  
12. [License](#license)

---

## **Project Overview**
**Your_Name’s Droid** is a Slack chatbot designed to handle questions in any channel it’s added to and mentioned in (`@Your_Name’s Droid`). When a user tags the bot, it sends the query along with the last 5 messages (both user and bot responses) to a Large Language Model (LLM), such as **OpenAI** or **Google Gemini**, to generate a contextual answer. The bot then replies directly in the Slack channel.

This repository fulfills the following requirements:
1. Listens to any question in a channel (where the bot is added & tagged).
2. For each question, sends **the current message + the last 5 messages** to an LLM.
3. Responds in the channel with an AI-generated reply.
4. Provides an **install link** so anyone can add the bot to their own Slack workspace.
5. Includes an **architecture diagram**, **codebase**, and a **demo video** showcasing functionality.
6. **Bonus**: The last 5 messages include both **user messages** and **bot responses**.

---

## **Key Features**
- **Context-Aware**: Includes the most recent conversation history (up to 5 messages) to produce relevant replies.
- **LLM-Integrated**: Easily swap between OpenAI, Google Gemini, or any other LLM of your choice.
- **Slack Mentions**: Listens for `@Your_Name’s Droid` mentions and replies in real-time.
- **Extensible**: Use Redis/PostgreSQL or in-memory storage for chat history, and adapt to advanced features like slash commands or Slack Block Kit.
- **Production-Ready**: FastAPI-based backend, easily deployable to services like Railway, Render, or AWS.

---

## **Architecture Diagram**
Below is a high-level overview of the system:

```
┌─────────────────────┐       ┌─────────────────────────┐
│     Slack User      │       │   Google Gemini / OpenAI│
│  (asks a question)  │       │     (Any LLM Provider)  │
└─────────┬───────────┘       └────────────┬────────────┘
          │                                │
          │  @mention + user question      │
          │                                │
          ▼                                │
 ┌───────────────────┐                     │
 │   Slack Backend   │                     │
 │ (Events API call) │                     │
 └─────────┬─────────┘                     │
           │  sends event (JSON)          │
           ▼                                │
┌────────────────────────────────────────────────┐
│           FastAPI Application                │
│                                              │
│  1) Receive Slack event                      │
│  2) Retrieve last 5 messages (user+bot)      │
│  3) Send prompt to LLM                       │
│  4) Receive AI response                      │
│  5) Post message in Slack channel            │
└────────────────────────────────────────────────┘
```

> **Note**: You can find the full-resolution image in the `static/` folder of this repo.

---

## **Installation & Setup**
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/YourGitHubUsername/your-names-droid.git
   cd your-names-droid
   ```

2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**  
   Create a `.env` file (or set environment variables) with the following keys:
   ```bash
   SLACK_BOT_TOKEN=your-slack-bot-token
   SLACK_SIGNING_SECRET=your-slack-signing-secret
   OPENAI_API_KEY=your-openai-api-key     # or
   GEMINI_API_KEY=your-gemini-api-key     # if using Google Gemini
   REDIS_URL=redis://localhost:6379       # optional if using Redis
   ```
   > Replace these with your actual keys/secrets.

4. **Run the Application**  
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   > Use [ngrok](https://ngrok.com/) to expose your local server for Slack Event Subscriptions if testing locally.

5. **Configure Slack Events**  
   - Go to your Slack App settings → **Event Subscriptions** → **Enable Events**.
   - Add your **Request URL** (e.g., `https://<YOUR-NGROK-URL>/slack/events`).
   - Subscribe to the event `app_mention` (and `message.channels` if you want full channel messages).
   - Save changes.

6. **Add Bot to Slack Channel**  
   - Go to your Slack workspace.
   - Invite the bot to a channel: `/invite @Your_Name’s Droid`.

---

## **Slack App Installation Link**
Share this link so others can add **Your_Name’s Droid** to their Slack workspace:

```
https://slack.com/oauth/v2/authorize?
client_id=YOUR_CLIENT_ID&
scope=app_mentions:read,channels:history,chat:write&
redirect_uri=YOUR_REDIRECT_URL
```

1. Replace `YOUR_CLIENT_ID` and `YOUR_REDIRECT_URL` with your actual Slack app credentials.
2. Anyone clicking this link can **Install the Bot** in their workspace.
3. They can then mention `@Your_Name’s Droid` to interact with your chatbot.

---

## **Usage**
1. **Mention the Bot**: Type `@Your_Name’s Droid <Your Question>` in a channel where the bot is present.
2. **Context-Aware Answers**: The bot automatically retrieves the **last 5 messages** (both user & bot responses) to give a contextual reply.
3. **Check Logs**: View the FastAPI server logs to see inbound Slack events and the LLM responses.

---

## **Video Demonstration**
**[Video Demo Link](https://www.loom.com/share/YourDemoLink)**  
- Demonstrates how the bot is installed in Slack.  
- Shows a user asking multiple questions.  
- Displays the bot’s context-aware replies.  

*(Replace with your actual video link—Loom, YouTube, or any hosting platform.)*

---

## **Repository Structure**
```
your-names-droid/
│── main.py                 # FastAPI backend
│── slack_events.py         # Slack event handling
│── gemini_api.py           # (Optional) Google Gemini integration
│── openai_api.py           # (Optional) OpenAI integration
│── storage.py              # Stores last 5 messages (user + bot)
│── requirements.txt        # Project dependencies
│── Dockerfile              # Containerize (optional)
│── README.md               # Documentation (you are here)
│── static/
│   └── architecture.png    # Architecture diagram
└── .env.example            # Sample environment variables
```

- **`main.py`**: Core FastAPI application with endpoints.  
- **`slack_events.py`**: Contains logic for processing Slack events and posting responses.  
- **`gemini_api.py`** / **`openai_api.py`**: LLM-specific code for generating responses.  
- **`storage.py`**: Simple in-memory or Redis-based storage for last 5 messages.  

---

## **How It Works**
1. **Slack → FastAPI**: User tags the bot in a Slack channel. Slack sends an event (JSON) to the FastAPI endpoint `/slack/events`.  
2. **Message Storage**: We store the user message and retrieve the previous 5 messages from the same channel (including the bot’s own replies).  
3. **LLM Call**: We combine those 5 messages + the new question into a prompt and send it to an LLM (OpenAI or Gemini).  
4. **Bot Reply**: The LLM returns a context-aware answer, which we post back to the Slack channel as the bot.

---

## **Future Improvements**
- **Enhanced Memory**: Persist entire conversation threads in a database for deeper context.  
- **Slash Commands**: Extend functionality (e.g., `/ask-droid` to ask private queries).  
- **Slack Block Kit**: Make responses more interactive with buttons, menus, or images.  
- **Analytics Dashboard**: Track usage, top queries, or user feedback.  

---

## **Contributing**
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change. Ensure that you update tests as appropriate.

---

## **License**
This project is licensed under the [MIT License](LICENSE).  

<br/>

---

**Thank you for checking out “Your_Name’s Droid”!**  

- **Feel free to install the bot** in your Slack workspace using the [installation link](#slack-app-installation-link).  
- **Watch the [video demo](#video-demonstration)** to see the chatbot in action.  
- **Contact**: For any questions or feedback, reach out via [GitHub Issues](../../issues) or email me at `YourEmail@domain.com`.  

> If you find this project helpful, please give it a ⭐ on GitHub.  