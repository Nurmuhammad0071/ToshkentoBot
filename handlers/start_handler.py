"""
Start command handler.
"""
import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from services.user_storage import UserStorage


logger = logging.getLogger(__name__)
router = Router()


# Welcome message for /start command
WELCOME_MESSAGE = """Салом!

Бу ерга ҳар қандай янгиликни юборишингиз мумкин: матн, фото, видео ёки аудио.

💁🏻‍♂️ Албатта, манзил, жой, содир бўлган ҳодиса ва вақти ҳақида маълумот беришни унутманг."""


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Handle /start command and save user data."""
    if not message.from_user:
        logger.warning("Received /start command without from_user")
        await message.answer(WELCOME_MESSAGE)
        return
    
    # Save user data
    try:
        is_new_user = UserStorage.save_user(message.from_user)
        if is_new_user:
            logger.info(f"New user started bot: {message.from_user.id}")
        else:
            logger.info(f"Existing user started bot: {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error saving user data: {e}", exc_info=True)
    
    # Send welcome message
    await message.answer(WELCOME_MESSAGE)

