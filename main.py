from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, InlineQueryHandler
from bot.config import get_telegram_token, get_default_target_lang
from bot.handlers import start, inline_query
from bot.database import init_database


def main() -> None:
    # Load environment variables
    load_dotenv()
    load_dotenv(".env.example", override=False)

    # Initialize database
    init_database()

    token = get_telegram_token()
    default_lang = get_default_target_lang()

    application = ApplicationBuilder().token(token).build()

    # Store default language in bot_data
    application.bot_data['default_target_lang'] = default_lang

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(InlineQueryHandler(inline_query))

    # Add admin command (ixtiyoriy)
    # application.add_handler(CommandHandler("stats", stats))

    print("🤖 Bot is starting with SQLite database...")
    print(f"📝 Default target language: {default_lang}")
    print(f"💾 Database file: bot_users.db")

    application.run_polling()


if __name__ == "__main__":
    main()
