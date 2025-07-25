# Telegram Bot

## Description

This project is a personal Telegram assistant bot written in Python, featuring a wide range of functions to help users with everyday tasks.

## Advantages

- **Integration with external APIs:**
  - Get up-to-date weather via Open-Meteo and geocoding via Nominatim.
  - Work with currency rates via the Apilayer API.
  - Translate text using Google Cloud Translate.
  - Generate responses using OpenAI GPT-4o-mini.
  - Get random images from external services (TheCatAPI).
- **Integration with Google Sheets:**
  - Save user data directly to Google Sheets for further analysis or storage.
- **Asynchronous architecture:**
  - High performance and responsiveness thanks to asynchronous libraries (aiogram, httpx).
- **Flexible user message handling:**
  - Dialogue history, personalized responses, natural language support.

## Setup
1. Create a `.env` file and specify your tokens:
   - `BOT_TOKEN` — Telegram bot token
   - `OPENAI_API_KEY` — OpenAI key (optional)
2. Place the Google service account file (`service.json`) in the project folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

![Bot Image](image.png)
