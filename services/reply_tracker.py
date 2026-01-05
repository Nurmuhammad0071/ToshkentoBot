"""
Reply tracking service to map group messages to users.
"""
from typing import Dict, Optional


class ReplyTracker:
    """
    Tracks message IDs in support group to map replies to users.
    Structure: {group_message_id: user_id}
    """
    
    def __init__(self):
        """Initialize reply tracker."""
        self._message_map: Dict[int, int] = {}
    
    def add_mapping(self, group_message_id: int, user_id: int) -> None:
        """
        Add mapping between group message ID and user ID.
        
        Args:
            group_message_id: Message ID in support group
            user_id: User ID who sent the original message
        """
        self._message_map[group_message_id] = user_id
    
    def get_user_id(self, group_message_id: int) -> Optional[int]:
        """
        Get user ID by group message ID.
        
        Args:
            group_message_id: Message ID in support group
        
        Returns:
            User ID if found, None otherwise
        """
        return self._message_map.get(group_message_id)
    
    def remove_mapping(self, group_message_id: int) -> None:
        """
        Remove mapping (cleanup).
        
        Args:
            group_message_id: Message ID in support group
        """
        self._message_map.pop(group_message_id, None)
    
    def clear_old_mappings(self, keep_last: int = 1000) -> None:
        """
        Clear old mappings, keep only last N.
        
        Args:
            keep_last: Number of recent mappings to keep
        """
        if len(self._message_map) > keep_last:
            # Keep only last N items
            items = list(self._message_map.items())[-keep_last:]
            self._message_map = dict(items)


# Global instance
reply_tracker = ReplyTracker()

