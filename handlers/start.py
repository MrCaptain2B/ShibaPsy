"""handlers/start.py — команда /start и callback/reply кнопки."""

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from keyboards import main_menu, main_reply_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    name = message.from_user.first_name or "друг"
    await message.answer(
        f"Привет, {name}! 👋\n\n"
        "Я — бот психологической поддержки. "
        "Я здесь, чтобы выслушать тебя и помочь разобраться в чувствах.\n\n"
        "Выбери, с чего начнём:",
        reply_markup=main_menu(),
    )
    # Показываем постоянную клавиатуру
    await message.answer(
        "Кнопки внизу всегда доступны 👇",
        reply_markup=main_reply_keyboard(),
    )


# ── Inline callback-кнопки ────────────────────────────────────────────────

@router.callback_query(lambda c: c.data == "menu_chat")
async def cb_chat(call: CallbackQuery) -> None:
    await call.answer()
    await call.message.answer(
        "Я слушаю тебя. Напиши, что тебя беспокоит, "
        "или просто поделись тем, что у тебя на душе. 💙\n\n"
        "Чтобы начать заново — нажми кнопку «Сбросить диалог»."
    )


@router.callback_query(lambda c: c.data == "menu_daily")
async def cb_daily(call: CallbackQuery) -> None:
    await call.answer()
    from handlers.daily import send_daily_advice
    await send_daily_advice(call.message)


# ── /help ──────────────────────────────────────────────────────────────────

_HELP_TEXT = (
    "❓ <b>Помощь по командам</b>\n\n"
    "💬 <b>Чат с ИИ</b> — просто напиши мне, я выслушаю и поддержу.\n"
    "💡 <b>Совет дня</b> — короткий психологический совет.\n"
    "🔄 <b>Сбросить диалог</b> — начать разговор с чистого листа.\n"
    "❓ <b>Помощь</b> — это сообщение.\n\n"
    "— Если тебе плохо, я всегда здесь. 💙\n"
    "— В критической ситуации набери <b>8-800-2000-122</b> (круглосуточно, бесплатно)."
)


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(_HELP_TEXT)


@router.callback_query(lambda c: c.data == "menu_help")
async def cb_help(call: CallbackQuery) -> None:
    await call.answer()
    await call.message.answer(_HELP_TEXT)


@router.message(F.text == "❓ Помощь")
async def reply_help(message: Message) -> None:
    await message.answer(_HELP_TEXT)


# ── Reply-кнопки (постоянная клавиатура) ─────────────────────────────────

@router.message(F.text == "💬 Чат с ИИ")
async def reply_chat(message: Message) -> None:
    await message.answer(
        "Я слушаю тебя. Напиши, что тебя беспокоит, "
        "или просто поделись тем, что у тебя на душе. 💙"
    )


@router.message(F.text == "💡 Совет дня")
async def reply_daily(message: Message) -> None:
    from handlers.daily import send_daily_advice
    await send_daily_advice(message)


@router.message(F.text == "🔄 Сбросить диалог")
async def reply_reset(message: Message) -> None:
    from database import reset_user_dialog
    await reset_user_dialog(message.from_user.id)
    await message.answer(
        "🔄 История нашего разговора очищена. Можем начать с чистого листа. 💙"
    )
