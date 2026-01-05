"""
Reply handler for processing replies from support group.
"""
import html
import logging
from aiogram import Router, F
from aiogram.types import Message
from config import Config
from services.reply_tracker import reply_tracker

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.chat.type.in_(["group", "supergroup"]))
async def handle_group_reply(message: Message) -> None:
    """
    Handle replies in support group and forward to user.
    Only process messages that are replies to tracked messages.
    """
    try:
        # Check if message is a reply
        if not message.reply_to_message:
            return
        
        # Check if message is in support group
        support_group_id = Config.get_support_group_id()
        if message.chat.id != support_group_id:
            return
        
        # Get the replied message ID
        replied_message_id = message.reply_to_message.message_id
        
        # Find user ID from reply tracker
        user_id = reply_tracker.get_user_id(replied_message_id)
        
        if not user_id:
            # Try to find from original forwarded message
            if message.reply_to_message.forward_from:
                user_id = message.reply_to_message.forward_from.id
                # Add to tracker for future replies
                reply_tracker.add_mapping(replied_message_id, user_id)
                logger.info(f"Found user {user_id} from forward_from, mapped message {replied_message_id}")
            else:
                # Try to find from reply chain - check if replied message is also a reply
                if message.reply_to_message.reply_to_message:
                    parent_id = message.reply_to_message.reply_to_message.message_id
                    user_id = reply_tracker.get_user_id(parent_id)
                    if user_id:
                        # Map this message too
                        reply_tracker.add_mapping(replied_message_id, user_id)
                        logger.info(f"Found user {user_id} from reply chain, mapped message {replied_message_id}")
                
                if not user_id:
                    # Last attempt: check all recent messages in the thread
                    # This helps with old messages that might not be in tracker
                    logger.warning(f"Could not find user for reply to message {replied_message_id}")
                    # Still try to send if we can find user from any source
                    # But don't return - let it fail gracefully
                    return
        
        # Format reply message - always use "Toshkento" as sender name
        operator_name = "Toshkento"
        
        # Prepare reply text (HTML format)
        if message.text:
            escaped_text = html.escape(message.text)
            reply_text = f"💬 <b>{operator_name}:</b>\n\n{escaped_text}"
        elif message.caption:
            escaped_caption = html.escape(message.caption)
            reply_text = f"💬 <b>{operator_name}:</b>\n\n{escaped_caption}"
        else:
            reply_text = f"💬 <b>{operator_name}</b> javob berdi:"
        
        # Send reply to user
        try:
            if message.text or message.caption:
                # Text message
                await message.bot.send_message(
                    chat_id=user_id,
                    text=reply_text,
                    parse_mode="HTML"
                )
            else:
                # Media message - forward with caption
                if message.caption:
                    escaped_caption = html.escape(message.caption)
                    await message.bot.send_message(
                        chat_id=user_id,
                        text=f"💬 <b>Toshkento:</b>\n\n{escaped_caption}",
                        parse_mode="HTML"
                    )
                
                # Forward media
                await message.forward(chat_id=user_id)
            
            # Confirm to operator (optional - can be removed)
            logger.info(f"Reply from {operator_name} sent to user {user_id}")
            
        except Exception as e:
            logger.error(f"Failed to send reply to user {user_id}: {e}")
            # Try to notify operator
            try:
                await message.reply(
                    f"❌ Xatolik: Foydalanuvchiga javob yuborib bo'lmadi. "
                    f"Ehtimol, foydalanuvchi botni bloklagan."
                )
            except:
                pass
        
    except Exception as e:
        logger.error(f"Error handling group reply: {e}", exc_info=True)

