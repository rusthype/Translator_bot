import sqlite3
from tabulate import tabulate

conn = sqlite3.connect('bot_users.db')
cursor = conn.cursor()

print("\n=== USERS ===")
cursor.execute(
    "SELECT user_id, username, first_name, total_queries, total_translations, last_seen FROM users ORDER BY last_seen DESC LIMIT 10")
users = cursor.fetchall()
print(tabulate(users, headers=['User ID', 'Username', 'Name', 'Queries', 'Translations', 'Last Seen']))

print("\n=== RECENT TRANSLATIONS ===")
cursor.execute("""
    SELECT u.username, t.original_text, t.translated_text, t.source_lang, t.target_lang, t.timestamp 
    FROM translations t
    JOIN users u ON t.user_id = u.user_id
    ORDER BY t.timestamp DESC LIMIT 5
""")
trans = cursor.fetchall()
print(tabulate(trans, headers=['User', 'Original', 'Translated', 'From', 'To', 'Time']))

conn.close()
