"""
Start command handler.
"""
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


# Welcome message for /start command
WELCOME_MESSAGE = """Салом!

Бу ерга ҳар қандай янгиликни юборишингиз мумкин: матн, фото, видео ёки аудио.

💁🏻‍♂️ Албатта, манзил, жой, содир бўлган ҳодиса ва вақти ҳақида маълумот беришни унутманг."""


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Handle /start command."""
    await message.answer(WELCOME_MESSAGE)

