"""handlers/media.py — ответ на нетекстовые сообщения."""

from aiogram import Router, F
from aiogram.types import Message

router = Router()

_REPLY = "Пожалуйста, напишите текстовое сообщение. ✏️"


@router.message(F.sticker)
async def on_sticker(message: Message) -> None:
    await message.reply(_REPLY)


@router.message(F.photo)
async def on_photo(message: Message) -> None:
    await message.reply(_REPLY)


@router.message(F.voice)
async def on_voice(message: Message) -> None:
    await message.reply(_REPLY)


@router.message(F.video)
async def on_video(message: Message) -> None:
    await message.reply(_REPLY)


@router.message(F.document)
async def on_document(message: Message) -> None:
    await message.reply(_REPLY)


@router.message(F.audio)
async def on_audio(message: Message) -> None:
    await message.reply(_REPLY)


@router.message(F.video_note)
async def on_video_note(message: Message) -> None:
    await message.reply(_REPLY)
