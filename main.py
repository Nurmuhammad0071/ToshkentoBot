"""
Main entry point for the Telegram Support Bot.
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import Config
from handlers import start_router, message_router, reply_router
from services.reply_tracker import reply_tracker


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Main function to start the support bot."""
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return
    
    # Create bot and dispatcher
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher()
    
    # Register routers (order matters - more specific first)
    # Start handler should come first to catch /start commands
    dp.include_router(start_router)
    # Reply handler for group messages
    dp.include_router(reply_router)
    # Message handler for private messages (should catch all other private messages)
    dp.include_router(message_router)
    
    try:
        bot_info = await bot.get_me()
        logger.info(f"🤖 Support Bot started: @{bot_info.username}")
        logger.info(f"📋 Support Group ID: {Config.SUPPORT_GROUP_ID}")
        logger.info(f"👥 Admin IDs: {Config.ADMIN_IDS if Config.ADMIN_IDS else 'Not set'}")
        
        # Start polling
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("🛑 Stopping bot...")
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
    finally:
        # Cleanup
        reply_tracker.clear_old_mappings()
        await bot.session.close()
        logger.info("✅ Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
