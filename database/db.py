"""
database/db.py — SQLite через aiosqlite.

Таблицы:
  dialogs       — история диалогов (user_id, role, content)
  daily_advices — кэш советов дня
"""

import aiosqlite
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "psybot.db"


async def init_db() -> None:
    """Создаёт таблицы при первом запуске."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS dialogs (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                role       TEXT    NOT NULL,
                content    TEXT    NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS daily_advices (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                content    TEXT    NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute(
            "CREATE INDEX IF NOT EXISTS idx_dialogs_user ON dialogs(user_id)"
        )
        await db.commit()


# ─────────────────────────── dialogs ──────────────────────────────────────

async def add_message(user_id: int, role: str, content: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO dialogs (user_id, role, content) VALUES (?, ?, ?)",
            (user_id, role, content),
        )
        await db.commit()


async def get_recent_messages(user_id: int, limit: int = 10) -> list[dict]:
    """Возвращает последние N сообщений пользователя в хронологическом порядке."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """
            SELECT role, content FROM (
                SELECT role, content, created_at
                FROM dialogs
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ) ORDER BY created_at ASC
            """,
            (user_id, limit),
        ) as cursor:
            rows = await cursor.fetchall()
    return [{"role": r["role"], "content": r["content"]} for r in rows]


async def cleanup_old_dialogs(days: int = 7) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM dialogs WHERE created_at < datetime('now', ?)",
            (f"-{days} days",),
        )
        await db.commit()


async def reset_user_dialog(user_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM dialogs WHERE user_id = ?", (user_id,))
        await db.commit()


# ─────────────────────────── daily_advices ────────────────────────────────

async def get_random_advice() -> str | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT content FROM daily_advices ORDER BY RANDOM() LIMIT 1"
        ) as cursor:
            row = await cursor.fetchone()
    return row["content"] if row else None


async def save_advice(content: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO daily_advices (content) VALUES (?)", (content,)
        )
        await db.commit()
