"""
Message handler for forwarding user messages to support group.
"""
import logging
from aiogram import Router, F
from aiogram.types import Message
from config import Config
from services.user_service import UserService
from services.message_service import MessageService
from services.reply_tracker import reply_tracker

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.chat.type == "private")
async def handle_private_message(message: Message) -> None:
    """
    Handle all private messages and forward to support group.
    Only process messages from private chats.
    Accepts messages from ALL users without any restrictions.
    """
    try:
        # Get user information
        user = message.from_user
        if not user:
            logger.warning("Message without from_user received")
            return
        
        # Log all incoming messages for debugging
        logger.info(f"Received message from user {user.id} (@{user.username or 'no_username'})")
        
        # Format user info
        # Check if message contains contact
        phone = None
        if message.contact:
            phone = message.contact.phone_number
        
        user_info = UserService.format_user_info(user, phone)
        
        # Get support group ID
        support_group_id = Config.get_support_group_id()
        
        # Check if message has media
        has_media = bool(message.photo or message.video or message.audio or 
                        message.voice or message.document or message.video_note or 
                        message.sticker or message.animation)
        
        # Format message for group
        formatted_message = MessageService.format_message_for_group(message, user_info)
        
        # Send formatted message to support group
        sent_message = None
        try:
            sent_message = await message.bot.send_message(
                chat_id=support_group_id,
                text=formatted_message,
                parse_mode="HTML"
            )
            # Track the formatted message ID
            reply_tracker.add_mapping(sent_message.message_id, user.id)
            logger.info(f"Formatted message sent to group, message_id: {sent_message.message_id}")
        except Exception as e:
            logger.error(f"Failed to send formatted message: {e}", exc_info=True)
        
        # Forward original message to group (for media/files)
        if has_media:
            try:
                forwarded = await message.forward(chat_id=support_group_id)
                # Track the forwarded message ID (this is the main one for replies)
                reply_tracker.add_mapping(forwarded.message_id, user.id)
                logger.info(f"Media forwarded to group, message_id: {forwarded.message_id}")
            except Exception as e:
                logger.error(f"Failed to forward media: {e}", exc_info=True)
        
        # Send confirmation to user
        await message.answer(
            "✅ Xabaringiz support guruhiga yuborildi. "
            "Tez orada javob olasiz!"
        )
        
        logger.info(f"Message from user {user.id} forwarded to support group")
        
    except Exception as e:
        logger.error(f"Error handling message: {e}", exc_info=True)
        try:
            await message.answer(
                "❌ Xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring."
            )
        except:
            pass

