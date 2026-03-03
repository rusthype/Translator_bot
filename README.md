## Telegram Inline Translator Bot

This is a **Python Telegram inline translator bot** that uses the **deep-translator** Python library (Google web translate under the hood). No Google Cloud account or credentials are required.

### Features

- Translate any text inline by typing `@YourBot text to translate` in any chat.
- Uses Google Cloud to auto-detect the source language.
- Replies with the translated text (default target language is English).

### 1. Prerequisites

- Python 3.10 or newer
- A Telegram bot token from BotFather
- Internet access (translations are performed via Google’s public web translate service)

### 2. Setup

1. **Clone or open this project directory**.
2. **Create and activate a virtual environment** (recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Create a Telegram bot** via BotFather and copy the bot token.
5. **Create a Google Cloud service account key** with access to Cloud Translation, download the JSON key file.

### 3. Configuration

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

Edit `.env`:

- `TELEGRAM_BOT_TOKEN` – your BotFather token.
- `DEFAULT_TARGET_LANG` – target language code (e.g. `en`, `es`, `de`).

Alternatively, you can export these variables directly in your shell instead of using `.env`.

### 4. Running the bot

With your virtual environment activated and environment variables set:

```bash
python main.py
```

You should see logs indicating that polling has started.

### 5. Using the bot

- Open Telegram and start a private chat with your bot; send `/start` to see basic help.
- In any chat, type:

```text
@tetristestwww_bot hello world
```

Replace `YourBotName` with your actual bot username. You should see an inline result with the translated text; tap it to send the translation into the chat.

### 6. Notes

- This bot uses an unofficial interface to Google Translate (via deep-translator); heavy or automated use may be rate-limited by Google.
- For production use, you may want to add per-user language settings, logging, and rate limiting.

