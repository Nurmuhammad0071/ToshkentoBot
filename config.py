"""
Configuration module for loading environment variables.
"""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""
    
    # Bot token
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    
    # Support group chat ID
    SUPPORT_GROUP_ID: str = os.getenv("SUPPORT_GROUP_ID", "")
    
    # Admin IDs (comma-separated)
    ADMIN_IDS: List[int] = []
    
    @classmethod
    def _parse_admin_ids(cls) -> List[int]:
        """Parse admin IDs from environment variable."""
        admin_ids_str = os.getenv("ADMIN_IDS", "")
        if not admin_ids_str:
            return []
        
        try:
            return [int(admin_id.strip()) for admin_id in admin_ids_str.split(",") if admin_id.strip()]
        except ValueError:
            return []
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN must be set in .env file")
        if not cls.SUPPORT_GROUP_ID:
            raise ValueError("SUPPORT_GROUP_ID must be set in .env file")
        
        # Parse admin IDs
        cls.ADMIN_IDS = cls._parse_admin_ids()
        
        return True
    
    @classmethod
    def get_support_group_id(cls) -> int:
        """Get support group ID as integer."""
        try:
            return int(cls.SUPPORT_GROUP_ID)
        except ValueError:
            raise ValueError(f"Invalid SUPPORT_GROUP_ID format: {cls.SUPPORT_GROUP_ID}")

