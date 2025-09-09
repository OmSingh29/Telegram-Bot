import logging
import os
import sys
import requests
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ChatAction
from dotenv import load_dotenv

# --- Configuration ---
# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if tokens are set
if not TELEGRAM_BOT_TOKEN:
    sys.exit("Error: TELEGRAM_BOT_TOKEN is not set in the environment variables.")
if not GEMINI_API_KEY:
    sys.exit("Error: GEMINI_API_KEY is not set in the environment variables.")

# Gemini API configuration
MODEL_NAME = "gemini-1.5-flash-latest"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"

# --- Conversation History Class ---
class ConversationHistory:
    """
    A class to store and manage the conversation history with the Gemini API.
    Gemini uses 'user' and 'model' roles.
    """
    def __init__(self) -> None:
        self.history = []

    def add_message(self, role: str, text: str):
        """Adds a new message to the history."""
        # We only add non-empty messages
        if text:
            self.history.append({"role": role, "parts": [{"text": text}]})

    def get_history(self):
        """Returns the current conversation history."""
        return self.history

    def clear(self):
        """Clears the conversation history."""
        self.history = []
        print("Conversation history has been cleared.")

# --- Bot Initialization ---
# Initialize conversation history instance
conversation = ConversationHistory()

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher()

logging.basicConfig(level=logging.INFO)

# --- Helper Functions ---
def clear_past():
    """A function to clear the previous conversation and context."""
    conversation.clear()

# --- Aiogram Handlers ---
@dispatcher.message(CommandStart())
async def welcome(message: types.Message):
    """
    This handler receives messages with the `/start` command.
    """
    await message.reply("Hi\nI am a Gemini-powered Tele Bot!\nCreated by Om Singh, adapted by an AI.\nHow can I assist you?")

@dispatcher.message(Command("clear"))
async def clear_command_handler(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")



@dispatcher.message(Command("help"))
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm a Gemini-powered Telegram bot! Please follow these commands:
    /start - To start the conversation.
    /clear - To clear the past conversation and context.
    /help - To get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)


@dispatcher.message()
async def gemini_handler(message: types.Message):
    """
    A handler to process the user's input and generate a response using the Gemini API.
    """
    print(f">>> USER: \n\t{message.text}")
    
    # Add user's message to conversation history
    conversation.add_message("user", message.text)

    # Prepare payload for the Gemini API
    payload = {"contents": conversation.get_history()}

    try:
        # Show a "typing..." action to the user
        await bot.send_chat_action(message.chat.id, action=ChatAction.TYPING)

        # Make the API call
        response = requests.post(GEMINI_API_URL, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

        # Extract the response text
        response_data = response.json()
        
        # A simple check for a valid response structure
        if 'candidates' in response_data and response_data['candidates']:
            gemini_response = response_data['candidates'][0]['content']['parts'][0]['text']
        else:
            # Handle cases with safety flags or no content
            gemini_response = "I couldn't generate a response for that. Please try something else."
            print(f"!!! API Error or empty response: {response_data}")


    except requests.exceptions.RequestException as e:
        gemini_response = f"An error occurred with the API request: {e}"
        print(f"!!! Request Exception: {e}")
    except Exception as e:
        gemini_response = f"An unexpected error occurred: {e}"
        print(f"!!! Unexpected Error: {e}")

    # Add Gemini's response to the conversation history
    conversation.add_message("model", gemini_response)

    print(f">>> GEMINI: \n\t{gemini_response}")
    await bot.send_message(chat_id=message.chat.id, text=gemini_response)

# --- Main Execution ---
async def main():
    """Starts the bot."""
    # Register handlers if you haven't already
    # This step is often done implicitly by decorators in simple bots,
    # but for clarity, know that handlers are registered with the dispatcher.

    # The `skip_updates=True` is now a parameter of `delete_webhook`.
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")

