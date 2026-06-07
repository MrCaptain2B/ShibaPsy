"""handlers/daily.py — команда /daily."""

import random

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services import generate_daily_advice

router = Router()

FALLBACK_ADVICES = [
    "Сделай сегодня одно маленькое доброе дело для себя. Ты этого заслуживаешь! 🌟",
    "Найди минуту, чтобы глубоко подышать и отпустить напряжение. Вдох — держи — выдох. 🌬️",
    "Напомни себе о трёх вещах, за которые ты благодарен прямо сейчас. Это меняет настрой. 🙏",
    "Небольшая прогулка на свежем воздухе способна изменить весь день к лучшему. 🚶",
    "Позволь себе сделать паузу. Отдых — это не слабость, а необходимость. ☕",
    "Напиши одному близкому человеку просто так — без повода. Связь с людьми лечит. 💙",
    "Сегодня достаточно просто быть. Не нужно всё успевать — ты уже делаешь достаточно. 🌿",
    "Выпей стакан воды прямо сейчас. Забота о теле — это тоже забота о душе. 💧",
    "Улыбнись себе в зеркало. Звучит странно, но это работает. 😊",
    "Позволь себе не быть идеальным сегодня. Прогресс важнее совершенства. ✨",
]


async def send_daily_advice(message: Message) -> None:
    thinking_msg = await message.answer("⏳ Подбираю совет для тебя...")

    try:
        advice = await generate_daily_advice()
        if not advice or len(advice) < 10:
            advice = random.choice(FALLBACK_ADVICES)
    finally:
        try:
            await thinking_msg.delete()
        except Exception:
            pass

    await message.answer(f"💡 Совет дня:\n\n{advice}")


@router.message(Command("daily"))
async def cmd_daily(message: Message) -> None:
    await send_daily_advice(message)
 