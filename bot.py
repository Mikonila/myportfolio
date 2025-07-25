import asyncio
import os
import httpx
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import Message
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import functools
from google.cloud import translate_v2 as translate
import openai
# from gigachat import GigaChat  
import json
import random

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Bot initialization
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Logging
logging.basicConfig(level=logging.INFO)

# Short-term memory
HISTORY_FILE = "history.json"

def load_history():
    print("Loading history...")
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                print("Loaded:", data)
                return data
        except Exception as e:
            print("Error reading history:", e)
            return {}
    return {}

def save_history(history):
    print("Saving history:", history)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def clean_history(history):
    # Removes messages with empty or non-string content
    return [
        msg for msg in history
        if isinstance(msg.get("content"), str) and msg.get("content").strip()
    ]

user_history = load_history()  # Load history once at startup

# Google Sheets — authorization
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"] 
creds = ServiceAccountCredentials.from_json_keyfile_name("service.json", scope)
client_gs = gspread.authorize(creds) 
sheet = client_gs.open("BotData").sheet1

# Google Translate client initialization
translate_client = translate.Client.from_service_account_json("service.json")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
# gigachat_client = GigaChat(credentials=YOUR_CREDENTIALS, verify_ssl_certs=False) 

def google_translate_sync(text, target="en"):
    result = translate_client.translate(text, target_language=target)
    return result["translatedText"]

@router.message(Command("start"))
async def start_cmd(message: Message):
    chat_id = str(message.chat.id)
    user_history[chat_id] = []
    await message.answer("Hello! I am a smart bot. Type /help to see what I can do.")

@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("/weather — weather\n/translate text — translate to English\n/currency — currency rates\n/cat — random cat photo\n/save text — save to Google Sheets\n/reset — clear history\nOr just send a message.")

@router.message(Command("reset"))
async def reset_history(message: Message):
    chat_id = str(message.chat.id)
    user_history[chat_id] = []
    save_history(user_history)
    await message.answer("History cleared.")

@router.message(Command("weather"))
async def weather_cmd(message: Message):
    city = message.text.replace("/weather", "").strip() or "Moscow"
    # Get coordinates via Nominatim
    geo_url = f"https://nominatim.openstreetmap.org/search"
    params = {"q": city, "format": "json", "limit": 1}
    async with httpx.AsyncClient() as client:
        geo_resp = await client.get(geo_url, params=params, headers={"User-Agent": "TelegramBot/1.0"})
        if geo_resp.status_code != 200 or not geo_resp.json():
            await message.answer(f"City '{city}' not found.")
            return
        geo = geo_resp.json()[0]
        lat, lon = geo["lat"], geo["lon"]
        # Get weather via Open-Meteo
        weather_url = f"https://api.open-meteo.com/v1/forecast"
        weather_params = {"latitude": lat, "longitude": lon, "current_weather": "true"}
        weather_resp = await client.get(weather_url, params=weather_params)
        if weather_resp.status_code != 200:
            await message.answer(f"Error getting weather: {weather_resp.status_code}\n{weather_resp.text}")
            return
        try:
            weather = weather_resp.json()["current_weather"]
            temp = weather["temperature"]
            wind = weather["windspeed"]
        except Exception as e:
            await message.answer(f"Error processing weather: {e}\n{weather_resp.text}")
            return
        await message.answer(f"Weather in {city}: {temp}°C, wind {wind} km/h")

@router.message(Command("translate"))
async def translate_cmd(message: Message):
    text = message.text.replace("/translate", "").strip()
    if not text:
        await message.answer("Please enter text after the command.")
        return
    loop = asyncio.get_running_loop()
    try:
        translated = await loop.run_in_executor(None, functools.partial(google_translate_sync, text, "en"))
    except Exception as e:
        await message.answer(f"Translation error: {e}")
        return
    await message.answer(f"Translation: {translated}")

@router.message(Command("currency"))
async def currency_cmd(message: Message):
    url = "https://api.apilayer.com/currency_data/live?source=USD&currencies=RUB,EUR"
    headers = {
        "apikey": "YqvudkhmHK1s4gqem0TYVByNaVAVXJD8"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            await message.answer(f"Error getting rates: {response.status_code}\n{response.text}")
            return
        try:
            data = response.json()
            if not data.get("success"):
                await message.answer(f"API error: {data.get('error', {}).get('info', 'Unknown error')}")
                return
            rub = data["quotes"]["USDRUB"]
            eur = data["quotes"]["USDEUR"]

        except Exception as e:
            await message.answer(f"Error processing response: {e}\n{response.text}")
            return
        await message.answer(f"1 RUB = {rub:.2f} USD / {eur:.2f} EUR")


@router.message(Command("cat"))
async def cat_cmd(message: Message):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.thecatapi.com/v1/images/search")
        if response.status_code == 200:
            data = response.json()
            cat_url = data[0]["url"]
            await message.answer_photo(cat_url)
        else:
            await message.answer("Could not get a cat :(")

@router.message(Command("save"))
async def save_to_gs(message: Message):
    text = message.text.replace("/save", "").strip()
    try:
        sheet.append_row([message.from_user.username or "unknown", text])
        await message.answer("Saved to the sheet.")
    except Exception as e:
        await message.answer(f"Error saving: {e}")

@router.message()
async def general_handler(message: Message):
    chat_id = str(message.chat.id)
    if chat_id not in user_history:
        user_history[chat_id] = []

    user_history[chat_id].append({"role": "user", "content": message.text})

    # length limit
    if len(user_history[chat_id]) > 10:
        user_history[chat_id] = user_history[chat_id][-10:]

    safe_history = clean_history(user_history[chat_id])

    if OPENAI_API_KEY:
        try:
            response = await openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=safe_history
            )
            answer = response.choices[0].message.content
            # response = await gigachat_client.chat(
            #     model="GigaChat:latest",
            #     messages=safe_history
            # )  # GigaChat: вызов метода chat
            # answer = response.choices[0]['message']['content']  # GigaChat: получение ответа
        except Exception as e:
            answer = f"Error generating answer: {e}"
    else:
        answer = "This is just a stub. Neural network response. (OPENAI_API_KEY not set)"

    user_history[chat_id].append({"role": "assistant", "content": answer})
    save_history(user_history)
    await message.answer(answer if answer is not None else "(No response from neural network)")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
