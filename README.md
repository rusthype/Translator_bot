# Telegram Inline Translator Bot

> Auto-translates messages between Uzbek, Russian, and English — works in any chat via inline mode.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.x-26A5E4?style=flat&logo=telegram&logoColor=white)](https://aiogram.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

---

## Features

- **Inline mode** — works in any Telegram chat without adding the bot to the group
- **Auto language detection** — no need to specify the source language
- **Three-way translation** — Uzbek ↔ Russian ↔ English
- **No paid API required** — powered by `deep-translator` (Google Translate backend)

## How It Works

Type the bot's name followed by your message in any Telegram chat:

```
@YourBot Salom, qanday yuribsiz?
```

The bot returns translation results inline — tap to send instantly.

```
→ Hello, how are you?
→ Привет, как дела?
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Bot framework | Aiogram 3 |
| Translation | deep-translator (Google Translate) |

---

## Quick Start

```bash
git clone https://github.com/rusthype/Translator_bot
cd Translator_bot
pip install -r requirements.txt
```

Create `.env`:

```env
BOT_TOKEN=your_telegram_bot_token
```

Run:

```bash
python main.py
```

---

## Usage

Open any Telegram chat (group, channel, or DM) and type `@YourBot` followed by the text you want translated. Select a translation from the inline results to send it.

Works without adding the bot to the chat — just mention it anywhere.

---

## Contributing

Pull requests are welcome. Report bugs or suggest features via [Issues](https://github.com/rusthype/Translator_bot/issues).

---

<div align="center">
  Made in Uzbekistan 🇺🇿 · <a href="https://alochi.org">alochi.org</a>
</div>
