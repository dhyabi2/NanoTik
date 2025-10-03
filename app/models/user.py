"""
User session and data models
"""

from typing import List, Dict, Any
from datetime import datetime
import uuid


class UserSession:
    """User session model for tracking user state"""
    
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.credits = 0
        self.videos = []
        self.transactions = []
    
    def add_credits(self, amount: int):
        """Add credits to user account"""
        self.credits += amount
    
    def deduct_credits(self, amount: int) -> bool:
        """
        Deduct credits from user account
        Returns True if successful, False if insufficient credits
        """
        if self.credits >= amount:
            self.credits -= amount
            return True
        return False
    
    def add_video(self, video_data: Dict[str, Any]):
        """Add a generated video to user's gallery"""
        video = {
            'id': str(uuid.uuid4()),
            'created_at': datetime.utcnow().isoformat(),
            **video_data
        }
        self.videos.append(video)
    
    def get_videos(self) -> List[Dict[str, Any]]:
        """Get all videos for this user"""
        return self.videos
    
    def add_transaction(self, transaction_data: Dict[str, Any]):
        """Record a payment transaction"""
        transaction = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat(),
            **transaction_data
        }
        self.transactions.append(transaction)
    
    def get_transaction_history(self) -> List[Dict[str, Any]]:
        """Get payment transaction history"""
        return self.transactions
