"""
main.py — точка входа бота психологической поддержки.

Запуск:
    python main.py
"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from database import init_db, cleanup_old_dialogs
from handlers import start, daily, chat, media
from services import ThrottlingMiddleware

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("BOT_TOKEN не задан в .env")
    if not os.environ.get("DEEPSEEK_API_KEY"):
        raise RuntimeError("DEEPSEEK_API_KEY не задан в .env")

    await init_db()
    await cleanup_old_dialogs(days=7)
    logger.info("База данных инициализирована. Устаревшие диалоги очищены.")

    bot = Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.message.outer_middleware(ThrottlingMiddleware())

    # Порядок важен: media и команды — до общего обработчика F.text
    dp.include_router(start.router)
    dp.include_router(daily.router)
    dp.include_router(media.router)
    dp.include_router(chat.router)

    logger.info("Бот запущен. Ожидаю сообщений...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
