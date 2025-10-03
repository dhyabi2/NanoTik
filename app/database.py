"""
Database module for NanoTik
Handles PostgreSQL connections and operations
"""

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

# Load environment variables from .env file
load_dotenv()


class Database:
    """Database connection and operations manager"""
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise Exception("DATABASE_URL not configured")
        self._ensure_tables()
    
    def get_connection(self):
        """Get a database connection"""
        return psycopg2.connect(self.database_url)
    
    def _ensure_tables(self):
        """Create tables if they don't exist"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                # Users table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id VARCHAR(36) PRIMARY KEY,
                        session_id VARCHAR(36) UNIQUE NOT NULL,
                        credits INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Videos table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS videos (
                        id VARCHAR(36) PRIMARY KEY,
                        user_id VARCHAR(36) REFERENCES users(id),
                        title VARCHAR(255) NOT NULL,
                        topic TEXT NOT NULL,
                        file_path TEXT NOT NULL,
                        duration INTEGER,
                        quality VARCHAR(50),
                        language VARCHAR(10),
                        status VARCHAR(50) DEFAULT 'completed',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Transactions table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS transactions (
                        id VARCHAR(36) PRIMARY KEY,
                        user_id VARCHAR(36) REFERENCES users(id),
                        transaction_type VARCHAR(50) NOT NULL,
                        amount NUMERIC(38, 18),
                        credits INTEGER NOT NULL,
                        currency VARCHAR(10),
                        payment_id VARCHAR(100) UNIQUE,
                        status VARCHAR(50) DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        completed_at TIMESTAMP
                    )
                """)
                
                # Create indexes for better query performance
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_videos_user_id ON videos(user_id)
                """)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id)
                """)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_transactions_payment_id ON transactions(payment_id)
                """)
                
                conn.commit()
    
    def create_user(self, session_id: str) -> Dict[str, Any]:
        """Create a new user"""
        user_id = str(uuid.uuid4())
        
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    INSERT INTO users (id, session_id, credits)
                    VALUES (%s, %s, 0)
                    RETURNING *
                """, (user_id, session_id))
                
                conn.commit()
                return dict(cur.fetchone())
    
    def get_user_by_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get user by session ID"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM users WHERE session_id = %s
                """, (session_id,))
                
                result = cur.fetchone()
                return dict(result) if result else None
    
    def update_user_credits(self, user_id: str, credits: int) -> bool:
        """Update user's credit balance"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE users SET credits = %s, last_active = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (credits, user_id))
                
                conn.commit()
                return cur.rowcount > 0
    
    def add_credits(self, user_id: str, amount: int) -> int:
        """Add credits to user and return new balance"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE users SET credits = credits + %s, last_active = CURRENT_TIMESTAMP
                    WHERE id = %s
                    RETURNING credits
                """, (amount, user_id))
                
                conn.commit()
                result = cur.fetchone()
                return result[0] if result else 0
    
    def deduct_credits(self, user_id: str, amount: int) -> bool:
        """Deduct credits from user if sufficient balance"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE users SET credits = credits - %s, last_active = CURRENT_TIMESTAMP
                    WHERE id = %s AND credits >= %s
                    RETURNING credits
                """, (amount, user_id, amount))
                
                conn.commit()
                return cur.rowcount > 0
    
    def create_video(self, user_id: str, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a video record"""
        video_id = str(uuid.uuid4())
        
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    INSERT INTO videos (id, user_id, title, topic, file_path, duration, quality, language, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING *
                """, (
                    video_id,
                    user_id,
                    video_data.get('title', ''),
                    video_data.get('topic', ''),
                    video_data.get('file_path', ''),
                    video_data.get('duration', 0),
                    video_data.get('quality', 'basic'),
                    video_data.get('language', 'en'),
                    video_data.get('status', 'completed')
                ))
                
                conn.commit()
                return dict(cur.fetchone())
    
    def get_user_videos(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all videos for a user"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM videos
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s
                """, (user_id, limit))
                
                return [dict(row) for row in cur.fetchall()]
    
    def create_transaction(self, user_id: str, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a transaction record"""
        transaction_id = str(uuid.uuid4())
        
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    INSERT INTO transactions (id, user_id, transaction_type, amount, credits, currency, payment_id, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING *
                """, (
                    transaction_id,
                    user_id,
                    transaction_data.get('transaction_type', 'purchase'),
                    transaction_data.get('amount', 0),
                    transaction_data.get('credits', 0),
                    transaction_data.get('currency', 'NANO'),
                    transaction_data.get('payment_id', ''),
                    transaction_data.get('status', 'pending')
                ))
                
                conn.commit()
                return dict(cur.fetchone())
    
    def update_transaction_status(self, transaction_id: str, status: str) -> bool:
        """Update transaction status"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE transactions 
                    SET status = %s, completed_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (status, transaction_id))
                
                conn.commit()
                return cur.rowcount > 0
    
    def get_user_transactions(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get transaction history for a user"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM transactions
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s
                """, (user_id, limit))
                
                return [dict(row) for row in cur.fetchall()]
    
    # Authentication methods
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM users WHERE email = %s
                """, (email,))
                
                result = cur.fetchone()
                return dict(result) if result else None
    
    def get_user_by_google_id(self, google_id: str) -> Optional[Dict[str, Any]]:
        """Get user by Google ID"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM users WHERE google_id = %s
                """, (google_id,))
                
                result = cur.fetchone()
                return dict(result) if result else None
    
    def create_authenticated_user(self, email: str, google_id: str, name: str, profile_picture: str = None) -> Dict[str, Any]:
        """Create a new authenticated user"""
        user_id = str(uuid.uuid4())
        session_id = str(uuid.uuid4())
        
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    INSERT INTO users (id, session_id, email, google_id, name, profile_picture, credits, has_used_trial)
                    VALUES (%s, %s, %s, %s, %s, %s, 0, FALSE)
                    RETURNING *
                """, (user_id, session_id, email, google_id, name, profile_picture))
                
                conn.commit()
                return dict(cur.fetchone())
    
    def use_free_trial(self, user_id: str) -> bool:
        """Mark user as having used their free trial"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE users SET has_used_trial = TRUE
                    WHERE id = %s AND has_used_trial = FALSE
                """, (user_id,))
                
                conn.commit()
                return cur.rowcount > 0
    
    # Splitroute invoice methods
    def create_splitroute_invoice(self, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a Splitroute invoice record"""
        invoice_record_id = str(uuid.uuid4())
        
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    INSERT INTO splitroute_invoices (
                        id, user_id, invoice_id, amount_nano, amount_usd, credits,
                        payment_address, status, expires_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING *
                """, (
                    invoice_record_id,
                    invoice_data.get('user_id'),
                    invoice_data.get('invoice_id'),
                    invoice_data.get('amount_nano'),
                    invoice_data.get('amount_usd', 0),
                    invoice_data.get('credits'),
                    invoice_data.get('payment_address'),
                    invoice_data.get('status', 'created'),
                    invoice_data.get('expires_at')
                ))
                
                conn.commit()
                return dict(cur.fetchone())
    
    def get_splitroute_invoice_by_id(self, invoice_id: str) -> Optional[Dict[str, Any]]:
        """Get Splitroute invoice by invoice ID"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM splitroute_invoices WHERE invoice_id = %s
                """, (invoice_id,))
                
                result = cur.fetchone()
                return dict(result) if result else None
    
    def update_splitroute_invoice_status(self, invoice_id: str, status: str, is_paid: bool = False) -> bool:
        """Update Splitroute invoice status"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                if is_paid:
                    cur.execute("""
                        UPDATE splitroute_invoices 
                        SET status = %s, is_paid = TRUE, paid_at = CURRENT_TIMESTAMP, webhook_verified = TRUE
                        WHERE invoice_id = %s
                    """, (status, invoice_id))
                else:
                    cur.execute("""
                        UPDATE splitroute_invoices 
                        SET status = %s
                        WHERE invoice_id = %s
                    """, (status, invoice_id))
                
                conn.commit()
                return cur.rowcount > 0


# Global database instance
_db_instance = None

def get_database() -> Database:
    """Get or create the global database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
