# Telegram Inline Translator Bot

> Inline Telegram bot — messages ni O'zbek, Rus va Ingliz tillariga avtomatik tarjima qiladi.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.x-26A5E4?style=flat&logo=telegram&logoColor=white)](https://aiogram.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

---

## Features

- **Inline mode** — any chat da `@BotUsername matn` yozish bilan ishlaydi
- **Auto language detection** — manba tilini avtomatik aniqlaydi
- **Multi-language** — O'zbek · Rus · Ingliz orasida tarjima
- **No API key required** — Google Cloud hisob raqami kerak emas

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.10+ |
| Bot framework | Aiogram 3 |
| Translation | deep-translator (Google Translate) |

## Quick Start

```bash
git clone https://github.com/rusthype/Translator_bot
cd Translator_bot
pip install -r requirements.txt
```

`.env` faylini yarating:

```env
BOT_TOKEN=your_telegram_bot_token
TARGET_LANG=en
```

Ishga tushirish:

```bash
python main.py
```

## Usage

Any Telegram chat da:

```
@YourBot Salom, qanday yuribsiz?
```

Bot avtomatik `Hello, how are you?` deb tarjima qilib beradi.

## Contributing

Pull request lar qabul qilinadi. [Issues](https://github.com/rusthype/Translator_bot/issues) da xatolik bildiring.

---

<div align="center">
  Made in Uzbekistan 🇺🇿 · <a href="https://alochi.org">alochi.org</a>
</div>
