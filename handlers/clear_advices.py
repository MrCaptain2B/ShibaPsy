"""
Запустить один раз для очистки устаревших советов из БД.
После запуска файл можно удалить.
"""
import asyncio
import aiosqlite
from pathlib import Path

DB_PATH = Path(__file__).parent / "psybot.db"


async def clear():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM daily_advices")
        await db.commit()
    print("✅ Таблица daily_advices очищена. Теперь советы будут генерироваться заново.")


asyncio.run(clear())