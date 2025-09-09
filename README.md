# Gemini-Powered Telegram Bot
A simple, yet powerful Telegram bot that uses Google's Gemini API (gemini-1.5-flash-latest) to provide intelligent, conversational responses. The bot maintains a conversation history to provide contextually aware answers.

# ✨ Features
Conversational AI: Leverages the Gemini API for natural and intelligent responses.

Conversation History: Remembers the context of the current conversation for more relevant replies.

Simple Commands: Easy-to-use commands to interact with the bot.

Asynchronous: Built with aiogram v3 for efficient, non-blocking operation.

Easy to Deploy: Can be deployed on various cloud platforms that support Python.

# 📋 Requirements
Python 3.11

A Telegram Bot Token

A Google Gemini API Key

# 🚀 Setup and Installation
Follow these steps to get your bot up and running.

1. Clone the Repository
   Clone this project to your local machine.
   ```
   git clone https://github.com/OmSingh29/Telegram-Bot.git
   ```

2. Create a Virtual Environment (Recommended):
   It's a good practice to create a virtual environment to manage project dependencies.

   # For Windows
      1. Using conda
         ```
         conda create -n Telegram_Bot python=3.11
         ```
         ```
         conda activate Telegram_Bot
         ```
      2. Without conda
         ```
         py -3.11 -m venv Telegram_Bot
         ```
         ```
         Telegram_Bot\Scripts\activate
         ```
   
   # For macOS/Linux
   ```
   python3.11 -m venv Telegram_Bot
   ```
   ```
   source Telegram_Bot/bin/activate
   ```

3. Install Dependencies
Install all the required Python packages using the requirements.txt file.
```
pip install -r requirements.txt
```

4. Set Up Environment Variables
   Create a file named .env in the root directory of the project. This file will store your secret API keys. Copy the contents of the .env.example file (if provided) or create it from scratch.

   Your .env file should look like this:
   
   TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE"
   GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
   
   TELEGRAM_BOT_TOKEN: Get this from the BotFather on Telegram.
   
   GEMINI_API_KEY: Get this from Google AI Studio.

# ▶️ How to Run the Bot
   Once you have completed the setup, you can start the bot by running the following command in your terminal:
   ```
   python telebot.py
   ```

   Your bot should now be online and responding to messages on Telegram!

# 🤖 Bot Commands
   /start - Initializes the bot and displays a welcome message.
   
   /help - Shows the help menu with a list of available commands.
   
   /clear - Clears the current conversation history, allowing you to start a fresh conversation.

This bot was created by Om Singh.
