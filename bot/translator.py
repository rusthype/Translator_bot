from typing import Any, Dict
from deep_translator import GoogleTranslator
from .config import get_default_target_lang

# Translator objekti global saqlanadi (har safar yaratilmaydi)
_translator_cache = {}


def translate_text(text: str, target_lang: str | None = None) -> Dict[str, Any]:
    """
    Translate text using deep-translator's GoogleTranslator.
    Optimized for speed.
    """
    text = (text or "").strip()
    if not text:
        return {
            "translated_text": "",
            "detected_source_language": None,
        }

    if target_lang is None:
        target_lang = get_default_target_lang()

    try:
        # Keshdan translator olish yoki yangi yaratish
        cache_key = f"auto_{target_lang}"
        if cache_key not in _translator_cache:
            _translator_cache[cache_key] = GoogleTranslator(source="auto", target=target_lang)

        translator = _translator_cache[cache_key]
        translated = translator.translate(text)

        return {
            "translated_text": translated,
            "detected_source_language": "auto",  # Google auto-detects
        }
    except Exception as e:
        # Xatolik bo'lganda
        return {
            "translated_text": f"[Error: {str(e)[:30]}]",
            "detected_source_language": None,
        }
