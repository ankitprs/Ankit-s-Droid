import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
# Load API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_gemini_response(history, user_message):
    """
    Calls the Gemini API with a system prompt and user input.
    
    :param system_prompt: Instructions for the AI's behavior.
    :param user_prompt: The user's message.
    :return: AI-generated response.
    """
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(
      model_name="gemini-1.5-flash-8b",
      system_instruction="You are Ankits Droid, a helpful AI assistant, and you are having a conversation with a user. Respond naturally and informatively.",
    )  
    prompt = f"Conversation history:\n{history}\n\nNew user message: {user_message}."

    try:
        response = model.generate_content([prompt])
        return response.text
    except Exception as e:
        return "I couldn't generate a response."
