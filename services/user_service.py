"""
User information service for formatting user data.
"""
import html
from typing import Optional
from aiogram.types import User


class UserService:
    """Service for user information formatting."""
    
    @staticmethod
    def get_user_full_name(user: User) -> str:
        """Get user's full name."""
        if user.first_name and user.last_name:
            return f"{user.first_name} {user.last_name}"
        return user.first_name or user.last_name or "Noma'lum"
    
    @staticmethod
    def get_user_username(user: User) -> str:
        """Get user's username with @."""
        if user.username:
            return f"@{user.username}"
        return "Yo'q"
    
    @staticmethod
    def get_user_phone(user: User) -> str:
        """Get user's phone number if available."""
        # Telegram API doesn't provide phone directly in User object
        # Phone is available only in contact messages
        return "Ko'rsatilmagan"
    
    @staticmethod
    def escape_html(text: str) -> str:
        """Escape HTML special characters."""
        if not text:
            return ""
        return html.escape(text)
    
    @staticmethod
    def format_user_info(user: User, phone: Optional[str] = None) -> str:
        """
        Format complete user information.
        
        Args:
            user: Telegram User object
            phone: Phone number if available (from contact message)
        
        Returns:
            Formatted user information string (HTML format)
        """
        full_name = UserService.escape_html(UserService.get_user_full_name(user))
        username = UserService.get_user_username(user)
        user_id = user.id
        phone_number = phone or UserService.get_user_phone(user)
        
        info = f"""
👤 <b>Foydalanuvchi ma'lumotlari:</b>

📝 <b>Ism:</b> {full_name}
🆔 <b>Username:</b> {username}
📱 <b>Telefon:</b> {phone_number}
🆔 <b>Telegram ID:</b> <code>{user_id}</code>
"""
        return info.strip()

