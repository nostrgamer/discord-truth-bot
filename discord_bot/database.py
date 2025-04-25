import sqlite3
from datetime import datetime
from typing import Optional, Dict, Any
import json
import os

class Database:
    """Database manager for storing monitoring configurations."""
    
    def __init__(self, db_path: str = "data/monitoring.db"):
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create monitoring_configs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS monitoring_configs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    filter_keyword TEXT NOT NULL,
                    last_checked_timestamp TEXT,
                    last_post_id TEXT,
                    created_at TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1
                )
            """)
            
            conn.commit()
    
    def add_monitoring_config(self, username: str, filter_keyword: str) -> int:
        """Add a new monitoring configuration."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO monitoring_configs 
                (username, filter_keyword, created_at, is_active)
                VALUES (?, ?, ?, 1)
            """, (username, filter_keyword, datetime.now().isoformat()))
            
            conn.commit()
            return cursor.lastrowid
    
    def get_monitoring_config(self) -> Optional[Dict[str, Any]]:
        """Get the current monitoring configuration."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM monitoring_configs 
                WHERE is_active = 1 
                ORDER BY created_at DESC 
                LIMIT 1
            """)
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'username': row[1],
                    'filter_keyword': row[2],
                    'last_checked_timestamp': row[3],
                    'last_post_id': row[4],
                    'created_at': row[5],
                    'is_active': bool(row[6])
                }
            return None
    
    def update_last_checked(self, post_id: str, timestamp: str):
        """Update the last checked timestamp and post ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE monitoring_configs 
                SET last_checked_timestamp = ?, last_post_id = ?
                WHERE is_active = 1
            """, (timestamp, post_id))
            
            conn.commit()
    
    def deactivate_monitoring(self):
        """Deactivate the current monitoring configuration."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE monitoring_configs 
                SET is_active = 0 
                WHERE is_active = 1
            """)
            
            conn.commit()
    
    def is_monitoring_active(self) -> bool:
        """Check if monitoring is currently active."""
        config = self.get_monitoring_config()
        return config is not None and config['is_active'] 