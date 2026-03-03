from telegram import Update
from telegram.ext import ContextTypes
from bot.database import get_all_users_count, get_today_active_users  # Absolute import
import sqlite3
import os

ADMIN_IDS = [8418578752]


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Admin command to see bot statistics"""
    if update.effective_user is None:
        return

    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    try:
        total_users = get_all_users_count()
        active_today = get_today_active_users()

        text = (
            f"📊 **Bot Statistics**\n\n"
            f"👥 **Total users:** {total_users}\n"
            f"📅 **Active today:** {active_today}\n"
        )

        await update.message.reply_text(text, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"❌ Error getting stats: {str(e)}")
