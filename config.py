import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# If the token is not found in .env, you can set it directly here
if not BOT_TOKEN:
    # Replace with your bot token
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        raise ValueError(
            "BOT_TOKEN is not set! "
            "Create a .env file with BOT_TOKEN=your_token_here "
            "or replace YOUR_BOT_TOKEN_HERE in config.py with your token"
        ) 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"
    if OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
        raise ValueError(
            "OPENAI_API_KEY is not set! "
            "Create a .env file with OPENAI_API_KEY=your_openai_key_here "
            "or replace YOUR_OPENAI_API_KEY_HERE in config.py with your key"
        ) 