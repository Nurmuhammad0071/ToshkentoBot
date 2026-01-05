"""
Yordamchi script: Guruh ID sini topish uchun.
Botni guruhga qo'shing va guruhda biror xabar yuboring.
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dp = Dispatcher()


@dp.message(Command("start"))
@dp.message()
async def get_chat_info(message: Message) -> None:
    """Guruh ID sini ko'rsatish."""
    chat = message.chat
    chat_id = chat.id
    chat_type = chat.type
    chat_title = getattr(chat, 'title', 'N/A')
    chat_username = getattr(chat, 'username', 'N/A')
    
    info = f"""
📋 Chat ma'lumotlari:

🆔 Chat ID: `{chat_id}`
📝 Chat Type: {chat_type}
📌 Title: {chat_title}
👤 Username: @{chat_username}

💡 .env faylida quyidagicha kiriting:
GROUP_CHAT_ID={chat_id}
"""
    
    await message.answer(info, parse_mode="Markdown")
    logger.info(f"Chat ID: {chat_id}, Type: {chat_type}, Title: {chat_title}")


async def main():
    """Main function."""
    bot = Bot(token=Config.BOT_TOKEN)
    
    try:
        bot_info = await bot.get_me()
        logger.info(f"🤖 Bot started: @{bot_info.username}")
        logger.info("📋 Guruhga qo'shing va biror xabar yuboring. Bot sizga guruh ID sini ko'rsatadi.")
        
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("🛑 Stopping...")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

