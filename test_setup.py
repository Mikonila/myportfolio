#!/usr/bin/env python3
"""
Test file for checking dependency installation
"""

def test_imports():
    """Checks that all required modules are installed"""
    try:
        import aiogram
        print("✅ aiogram installed successfully")
    except ImportError:
        print("❌ aiogram is not installed. Run: pip install aiogram")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv installed successfully")
    except ImportError:
        print("❌ python-dotenv is not installed. Run: pip install python-dotenv")
        return False
    
    try:
        from config import BOT_TOKEN
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            print("⚠️  Bot token is not set!")
            print("📝 Create a .env file with: BOT_TOKEN=your_token_here")
            print("📝 Or replace YOUR_BOT_TOKEN_HERE in config.py with your token")
            return False
        else:
            print("✅ Bot token is set")
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🔍 Checking Telegram bot setup...")
    print("=" * 50)
    
    if test_imports():
        print("=" * 50)
        print("✅ All set! You can run the bot:")
        print("   python bot.py")
        print("   or")
        print("   python advanced_bot.py")
    else:
        print("=" * 50)
        print("❌ There are problems with the setup. See instructions above.")

if __name__ == "__main__":
    main() 