import sqlite3
import datetime
import os
from typing import Dict, Any, Optional

DB_NAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bot_users.db")


def init_database():
    """Create database and tables if they don't exist"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            language_code TEXT,
            is_bot BOOLEAN,
            first_seen TIMESTAMP,
            last_seen TIMESTAMP,
            total_queries INTEGER DEFAULT 0,
            total_translations INTEGER DEFAULT 0
        )
    ''')

    # Translations table (history)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            original_text TEXT,
            translated_text TEXT,
            source_lang TEXT,
            target_lang TEXT,
            timestamp TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    # Queries table (inline queries history)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            query_text TEXT,
            timestamp TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    conn.commit()
    conn.close()
    print(f"✅ Database initialized: {DB_NAME}")


def add_or_update_user(user_data: Dict[str, Any]) -> None:
    """Add new user or update existing user's last_seen"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    now = datetime.datetime.now()
    user_id = user_data.get('id')

    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    existing = cursor.fetchone()

    if existing:
        # Update existing user
        cursor.execute('''
            UPDATE users 
            SET username = ?, first_name = ?, last_name = ?, 
                language_code = ?, last_seen = ?
            WHERE user_id = ?
        ''', (
            user_data.get('username', ''),
            user_data.get('first_name', ''),
            user_data.get('last_name', ''),
            user_data.get('language_code', ''),
            now,
            user_id
        ))
    else:
        # Insert new user
        cursor.execute('''
            INSERT INTO users 
            (user_id, username, first_name, last_name, language_code, is_bot, first_seen, last_seen, total_queries, total_translations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            user_data.get('username', ''),
            user_data.get('first_name', ''),
            user_data.get('last_name', ''),
            user_data.get('language_code', ''),
            user_data.get('is_bot', False),
            now,
            now,
            0,
            0
        ))

    conn.commit()
    conn.close()


def log_inline_query(user_id: int, query_text: str) -> None:
    """Log every inline query"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    now = datetime.datetime.now()

    # Insert query record
    cursor.execute('''
        INSERT INTO queries (user_id, query_text, timestamp)
        VALUES (?, ?, ?)
    ''', (user_id, query_text, now))

    # Update user's total queries count
    cursor.execute('''
        UPDATE users 
        SET total_queries = total_queries + 1,
            last_seen = ?
        WHERE user_id = ?
    ''', (now, user_id))

    conn.commit()
    conn.close()


def log_translation(user_id: int, original: str, translated: str, source: Optional[str], target: str) -> None:
    """Log every translation"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    now = datetime.datetime.now()

    # Insert translation record
    cursor.execute('''
        INSERT INTO translations 
        (user_id, original_text, translated_text, source_lang, target_lang, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, original, translated, source, target, now))

    # Update user's total translations count
    cursor.execute('''
        UPDATE users 
        SET total_translations = total_translations + 1
        WHERE user_id = ?
    ''', (user_id,))

    conn.commit()
    conn.close()


def get_user_stats(user_id: int) -> Dict[str, Any]:
    """Get statistics for a specific user"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT total_queries, total_translations, first_seen, last_seen
        FROM users WHERE user_id = ?
    ''', (user_id,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            'total_queries': result[0],
            'total_translations': result[1],
            'first_seen': result[2],
            'last_seen': result[3]
        }
    return {}


def get_all_users_count() -> int:
    """Get total number of users"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    conn.close()
    return count


def get_today_active_users() -> int:
    """Get number of users active today"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    today = datetime.datetime.now().date()
    cursor.execute('''
        SELECT COUNT(DISTINCT user_id) FROM queries 
        WHERE date(timestamp) = ?
    ''', (today,))

    count = cursor.fetchone()[0]
    conn.close()
    return count
