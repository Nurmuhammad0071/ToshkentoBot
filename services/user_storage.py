"""
User storage service for saving user data to JSON file.
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from aiogram.types import User


logger = logging.getLogger(__name__)

# Path to users JSON file
USERS_FILE = Path("data/users.json")


class UserStorage:
    """Service for storing user data in JSON file."""
    
    @staticmethod
    def _ensure_data_directory() -> None:
        """Ensure data directory exists."""
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def _load_users() -> Dict[str, dict]:
        """Load users from JSON file."""
        UserStorage._ensure_data_directory()
        
        if not USERS_FILE.exists():
            return {}
        
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading users file: {e}")
            return {}
    
    @staticmethod
    def _save_users(users: Dict[str, dict]) -> None:
        """Save users to JSON file."""
        UserStorage._ensure_data_directory()
        
        try:
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
        except IOError as e:
            logger.error(f"Error saving users file: {e}")
    
    @staticmethod
    def save_user(user: User) -> bool:
        """
        Save or update user data.
        
        Args:
            user: Telegram User object
            
        Returns:
            True if user was newly added, False if updated
        """
        users = UserStorage._load_users()
        user_id = str(user.id)
        current_time = datetime.now().isoformat()
        
        is_new_user = user_id not in users
        
        if is_new_user:
            # New user
            users[user_id] = {
                "user_id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "language_code": user.language_code,
                "is_bot": user.is_bot,
                "is_premium": getattr(user, "is_premium", False),
                "first_seen": current_time,
                "last_seen": current_time,
                "start_count": 1
            }
            logger.info(f"New user saved: {user.id} (@{user.username or 'no_username'})")
        else:
            # Existing user - update last_seen and increment start_count
            users[user_id]["last_seen"] = current_time
            users[user_id]["start_count"] = users[user_id].get("start_count", 0) + 1
            
            # Update user info if changed
            users[user_id]["username"] = user.username
            users[user_id]["first_name"] = user.first_name
            users[user_id]["last_name"] = user.last_name
            users[user_id]["language_code"] = user.language_code
            users[user_id]["is_premium"] = getattr(user, "is_premium", False)
            
            logger.info(f"User updated: {user.id} (@{user.username or 'no_username'}) - start_count: {users[user_id]['start_count']}")
        
        UserStorage._save_users(users)
        return is_new_user
    
    @staticmethod
    def get_user(user_id: int) -> Optional[dict]:
        """
        Get user data by user_id.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            User data dict or None if not found
        """
        users = UserStorage._load_users()
        return users.get(str(user_id))
    
    @staticmethod
    def get_all_users() -> Dict[str, dict]:
        """
        Get all users.
        
        Returns:
            Dictionary of all users
        """
        return UserStorage._load_users()
    
    @staticmethod
    def get_user_count() -> int:
        """
        Get total number of users.
        
        Returns:
            Number of users
        """
        return len(UserStorage._load_users())

