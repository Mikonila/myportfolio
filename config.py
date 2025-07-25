import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем токен бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Если токен не найден в .env, можно задать его напрямую здесь
if not BOT_TOKEN:
    # Замените на ваш токен бота
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        raise ValueError(
            "Не установлен BOT_TOKEN! "
            "Создайте файл .env с содержимым BOT_TOKEN=your_token_here "
            "или замените YOUR_BOT_TOKEN_HERE в config.py на ваш токен"
        ) 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"
    if OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
        raise ValueError(
            "Не установлен OPENAI_API_KEY! "
            "Создайте файл .env с содержимым OPENAI_API_KEY=your_openai_key_here "
            "или замените YOUR_OPENAI_API_KEY_HERE в config.py на ваш ключ"
        ) 