"""
Guruhni tekshirish scripti.
"""
import asyncio
import logging
from aiogram import Bot
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def check_group():
    """Guruhni tekshirish."""
    bot = Bot(token=Config.BOT_TOKEN)
    
    try:
        # Bot ma'lumotlarini olish
        bot_info = await bot.get_me()
        logger.info(f"🤖 Bot: @{bot_info.username} (ID: {bot_info.id})")
        
        # Guruh ID ni olish
        group_chat_id = Config.GROUP_CHAT_ID
        if isinstance(group_chat_id, str):
            try:
                group_chat_id = int(group_chat_id)
            except ValueError:
                logger.error(f"❌ GROUP_CHAT_ID noto'g'ri format: {Config.GROUP_CHAT_ID}")
                return
        
        logger.info(f"📋 Tekshirilayotgan guruh ID: {group_chat_id}")
        
        # Guruh ma'lumotlarini olish
        try:
            chat = await bot.get_chat(group_chat_id)
            logger.info(f"✅ Guruh topildi!")
            logger.info(f"   📌 Nomi: {chat.title}")
            logger.info(f"   🆔 ID: {chat.id}")
            logger.info(f"   📝 Type: {chat.type}")
            
            # Bot guruhda bormi tekshirish
            try:
                member = await bot.get_chat_member(group_chat_id, bot_info.id)
                logger.info(f"   ✅ Bot guruhda: {member.status}")
            except Exception as e:
                logger.warning(f"   ⚠️ Bot guruhda emas yoki admin huquqlari yo'q: {e}")
                logger.info("   💡 Botni guruhga qo'shing va admin qiling!")
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ Xatolik: {error_msg}")
            
            if "chat not found" in error_msg.lower():
                logger.error("   💡 Muammo: Guruh topilmadi!")
                logger.info("   Tekshiring:")
                logger.info("   1. Bot guruhga qo'shilganmi?")
                logger.info("   2. GROUP_CHAT_ID to'g'rimi?")
                logger.info("   3. Guruh mavjudmi?")
            elif "not enough rights" in error_msg.lower():
                logger.error("   💡 Muammo: Botda yetarli huquqlar yo'q!")
                logger.info("   Botni admin qiling yoki guruh sozlamalarini tekshiring.")
            else:
                logger.error(f"   💡 Boshqa xatolik: {error_msg}")
        
    except Exception as e:
        logger.error(f"❌ Umumiy xatolik: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(check_group())

