"""
Message formatting service for support bot.
"""
import html
from datetime import datetime
from typing import Optional
from aiogram.types import Message


class MessageService:
    """Service for message formatting."""
    
    @staticmethod
    def get_message_type(message: Message) -> str:
        """Get message type as string."""
        if message.text:
            return "📝 Text"
        elif message.photo:
            return "🖼️ Photo"
        elif message.video:
            return "🎥 Video"
        elif message.audio:
            return "🎵 Audio"
        elif message.voice:
            return "🎤 Voice"
        elif message.document:
            return "📄 Document"
        elif message.video_note:
            return "📹 Video Note"
        elif message.sticker:
            return "😊 Sticker"
        elif message.animation:
            return "🎬 Animation"
        elif message.location:
            return "📍 Location"
        elif message.contact:
            return "📞 Contact"
        else:
            return "❓ Noma'lum"
    
    @staticmethod
    def escape_html(text: str) -> str:
        """Escape HTML special characters."""
        if not text:
            return ""
        return html.escape(text)
    
    @staticmethod
    def get_message_content(message: Message) -> str:
        """Get message content preview."""
        if message.text:
            # Limit text length and escape HTML
            text = MessageService.escape_html(message.text[:200])
            if len(message.text) > 200:
                text += "..."
            return f"💬 {text}"
        elif message.caption:
            caption = MessageService.escape_html(message.caption[:200])
            if len(message.caption) > 200:
                caption += "..."
            return f"💬 {caption}"
        elif message.photo:
            return "🖼️ Rasm"
        elif message.video:
            return f"🎥 Video ({message.video.duration if message.video.duration else 'N/A'}s)"
        elif message.audio:
            title = message.audio.title or "Noma'lum"
            return f"🎵 Audio: {title}"
        elif message.voice:
            duration = message.voice.duration if message.voice.duration else "N/A"
            return f"🎤 Ovoz ({duration}s)"
        elif message.document:
            file_name = message.document.file_name or "Noma'lum"
            return f"📄 Fayl: {file_name}"
        else:
            return "📦 Media"
    
    @staticmethod
    def format_datetime(message: Message) -> str:
        """Format message date and time."""
        if message.date:
            dt = message.date
            formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
            return f"🕐 {formatted}"
        return "🕐 Noma'lum"
    
    @staticmethod
    def is_dangerous_file(message: Message) -> bool:
        """Check if file is potentially dangerous."""
        if message.document:
            file_name = message.document.file_name or ""
            file_ext = file_name.lower().split('.')[-1] if '.' in file_name else ""
            
            dangerous_extensions = ['apk', 'exe', 'bat', 'cmd', 'com', 'pif', 'scr', 'vbs', 'js']
            return file_ext in dangerous_extensions
        
        return False
    
    @staticmethod
    def format_message_for_group(message: Message, user_info: str) -> str:
        """
        Format complete message for support group.
        
        Args:
            message: Telegram Message object
            user_info: Formatted user information string
        
        Returns:
            Formatted message string
        """
        message_type = MessageService.get_message_type(message)
        message_content = MessageService.get_message_content(message)
        message_time = MessageService.format_datetime(message)
        is_dangerous = MessageService.is_dangerous_file(message)
        
        formatted = f"""
{user_info}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📨 <b>Xabar ma'lumotlari:</b>

{message_type}
{message_content}
{message_time}
"""
        
        if is_dangerous:
            formatted += "\n⚠️ <b>OGOHLANTIRISH:</b> Ushbu fayl zararli bo'lishi mumkin!"
        
        return formatted.strip()

