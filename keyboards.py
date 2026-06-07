"""keyboards.py — inline и reply клавиатуры."""

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def main_menu() -> InlineKeyboardMarkup:
    """Inline-кнопки для сообщения /start."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💬 Чат с ИИ",  callback_data="menu_chat"),
                InlineKeyboardButton(text="💡 Совет дня", callback_data="menu_daily"),
            ],
            [
                InlineKeyboardButton(text="❓ Помощь", callback_data="menu_help"),
            ],
        ]
    )


def main_reply_keyboard() -> ReplyKeyboardMarkup:
    """Постоянная клавиатура внизу экрана."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💬 Чат с ИИ"),
                KeyboardButton(text="💡 Совет дня"),
            ],
            [
                KeyboardButton(text="🔄 Сбросить диалог"),
                KeyboardButton(text="❓ Помощь"),
            ],
        ],
        resize_keyboard=True,        # компактный размер
        input_field_placeholder="Напишите что-нибудь...",
    )
 