#!/usr/bin/env python3
"""
Тестовый файл для проверки установки зависимостей
"""

def test_imports():
    """Проверяет, что все необходимые модули установлены"""
    try:
        import aiogram
        print("✅ aiogram установлен успешно")
    except ImportError:
        print("❌ aiogram не установлен. Выполните: pip install aiogram")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv установлен успешно")
    except ImportError:
        print("❌ python-dotenv не установлен. Выполните: pip install python-dotenv")
        return False
    
    try:
        from config import BOT_TOKEN
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            print("⚠️  Токен бота не настроен!")
            print("📝 Создайте файл .env с содержимым: BOT_TOKEN=ваш_токен_здесь")
            print("📝 Или замените YOUR_BOT_TOKEN_HERE в config.py на ваш токен")
            return False
        else:
            print("✅ Токен бота настроен")
    except Exception as e:
        print(f"❌ Ошибка при загрузке конфигурации: {e}")
        return False
    
    return True

def main():
    """Главная функция"""
    print("🔍 Проверка установки Telegram-бота...")
    print("=" * 50)
    
    if test_imports():
        print("=" * 50)
        print("✅ Все готово! Можно запускать бота:")
        print("   python bot.py")
        print("   или")
        print("   python advanced_bot.py")
    else:
        print("=" * 50)
        print("❌ Есть проблемы с установкой. Смотрите инструкции выше.")

if __name__ == "__main__":
    main() 