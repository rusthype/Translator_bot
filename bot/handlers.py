from uuid import uuid4
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ContextTypes
from bot.translator import translate_text
from bot.database import (  # Absolute import
    init_database, add_or_update_user, log_inline_query,
    log_translation, get_user_stats
)
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

# Initialize database when module loads
init_database()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.effective_user is None:
        return

    # Save user to database
    user = update.effective_user
    add_or_update_user({
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'language_code': user.language_code,
        'is_bot': user.is_bot
    })

    # Get user stats for personalized message
    stats = get_user_stats(user.id)

    text = (
        f"👋 Hi {user.first_name}! I am an inline translator bot.\n\n"
        f"📝 **Usage:**\n"
        f"- In any chat, type: `@tetristestwww_bot some text`\n"
        f"- I will return the translation (default target language is English).\n\n"
        f"📊 **Your stats:**\n"
        f"- Total queries: {stats.get('total_queries', 0)}\n"
        f"- Total translations: {stats.get('total_translations', 0)}\n"
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode='Markdown'
    )
    logging.info(f"Start command from user {user.id} ({user.username})")


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.inline_query is None or update.inline_query.from_user is None:
        return

    user = update.inline_query.from_user
    query = update.inline_query.query.strip() if update.inline_query.query else ""

    # Save user to database (asynchronous)
    await asyncio.to_thread(add_or_update_user, {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'language_code': user.language_code,
        'is_bot': user.is_bot
    })

    # Log the query (asynchronous)
    await asyncio.to_thread(log_inline_query, user.id, query)
    logging.info(f"Inline query from user {user.id}: '{query}'")

    # BO'SH QUERY - TEZ JAVOB
    if not query:
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Type text to translate",
                description="Example: hello world",
                input_message_content=InputTextMessageContent(
                    "Type some text after the bot username to translate it."
                ),
            )
        ]
        try:
            await update.inline_query.answer(results, cache_time=0, is_personal=True)
        except Exception as e:
            logging.error(f"Error answering empty query: {e}")
        return

    # TRANSLATION - TEZ JAVOB BERISH
    try:
        # Translatsiyani alohida threadda bajarish
        data = await asyncio.to_thread(translate_text, query)
        translated = data.get("translated_text") or ""
        detected = data.get("detected_source_language") or "auto"
        target = context.bot_data.get('default_target_lang', 'en')

        # Log translation (asynchronous)
        if translated and translated != "(empty translation)":
            await asyncio.to_thread(log_translation, user.id, query, translated, detected, target)

        if not translated:
            translated = "(empty translation)"

        title_preview = translated
        if len(title_preview) > 40:
            title_preview = title_preview[:37] + "..."

        description = f"Detected: {detected} • Original: {query[:30]}..."

        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=title_preview,
                description=description,
                input_message_content=InputTextMessageContent(translated),
            )
        ]

        # Javobni darhol yuborish
        await update.inline_query.answer(results, cache_time=0, is_personal=True)

    except Exception as exc:
        error_text = f"Translation failed: {str(exc)[:50]}..."
        logging.error(f"Translation error for user {user.id}: {exc}")

        # Xatolik bo'lganda ham tez javob berish
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="⚠️ Translation error",
                description="Tap to see error",
                input_message_content=InputTextMessageContent(error_text),
            )
        ]
        try:
            await update.inline_query.answer(results, cache_time=0, is_personal=True)
        except Exception as e:
            logging.error(f"Error answering error query: {e}")
