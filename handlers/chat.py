"""handlers/chat.py — основной чат с ИИ и команда /reset."""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest  # <-- Добавили импорт для отлова ошибок парсинга

from database import add_message, get_recent_messages, reset_user_dialog
from filters import is_crisis, CRISIS_RESPONSE
from services import chat_with_ai, split_long_message

router = Router()


@router.message(Command("reset"))
async def cmd_reset(message: Message) -> None:
    await reset_user_dialog(message.from_user.id)
    await message.answer(
        "🔄 История нашего разговора очищена. Можем начать с чистого листа. 💙"
    )


@router.message(F.text)
async def handle_text(message: Message) -> None:
    user_id = message.from_user.id
    user_text = message.text.strip()

    # ── Кризисный фильтр ──────────────────────────────────────────────
    if is_crisis(user_text):
        await message.answer(CRISIS_RESPONSE)
        return

    # ── Сохраняем сообщение пользователя ──────────────────────────────
    await add_message(user_id, "user", user_text)

    # ── Загружаем контекст ─────────────────────────────────────────────
    history = await get_recent_messages(user_id, limit=10)
    history_for_ai = history[:-1]

    # ── Отправляем сообщение-заглушку пока думаем ─────────────────────
    thinking_msg = await message.answer("⏳ Думаю над ответом...")

    # ── Запрос к DeepSeek ─────────────────────────────────────────────
    reply = await chat_with_ai(history_for_ai, user_text)

    # ── Удаляем заглушку ──────────────────────────────────────────────
    try:
        await thinking_msg.delete()
    except Exception:
        pass

    # ── Сохраняем ответ бота ───────────────────────────────────────────
    await add_message(user_id, "assistant", reply)

    # ── Отправляем с защитой от кривых HTML-тегов нейросети ───────────
    for part in split_long_message(reply):
        try:
            await message.answer(part)
        except TelegramBadRequest as e:
            # Если Telegram ругнулся на неподдерживаемый тег (вроде <rigidbody2d>)
            if "can't parse entities" in str(e):
                # Отправляем эту же часть, но принудительно отключаем HTML-парсинг
                await message.answer(part, parse_mode=None)
            else:
                # Если произошла какая-то другая ошибка, пробрасываем её дальше
                raise