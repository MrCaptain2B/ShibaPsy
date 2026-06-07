"""services/throttling.py — ограничение частоты сообщений."""

import asyncio
from collections import defaultdict

from aiogram import BaseMiddleware
from aiogram.types import Message


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: int = 5, time_window: float = 10.0):
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.user_timestamps: dict[int, list[float]] = defaultdict(list)
        super().__init__()

    async def __call__(self, handler, event: Message, data: dict) -> None:
        if not isinstance(event, Message):
            return await handler(event, data)

        user_id = event.from_user.id
        now = asyncio.get_event_loop().time()

        self.user_timestamps[user_id] = [
            t for t in self.user_timestamps[user_id]
            if now - t < self.time_window
        ]

        if len(self.user_timestamps[user_id]) >= self.rate_limit:
            await event.answer(
                "Пожалуйста, не так быстро. Я ещё обрабатываю предыдущие сообщения."
            )
            return

        self.user_timestamps[user_id].append(now)
        return await handler(event, data)
