"""User profile and personalization system"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from core.logger import setup_logger

logger = setup_logger("UserProfile")


class UserProfile:
    """Manages user profile and personalization"""
    
    def __init__(self, data_dir: Path, user_name: str = "User"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.db_path = self.data_dir / "user_profile.db"
        self.user_name = user_name
        
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Conversation history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                assistant_response TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User habits/patterns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_data TEXT,
                frequency INTEGER DEFAULT 1,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info("User profile database initialized")
    
    def set_preference(self, key: str, value: Any):
        """Set user preference"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO preferences (key, value, updated_at)
            VALUES (?, ?, ?)
        """, (key, json.dumps(value), datetime.now()))
        
        conn.commit()
        conn.close()
        logger.info(f"Preference set: {key}")
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT value FROM preferences WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return json.loads(row[0])
        return default
    
    def save_conversation(self, user_input: str, assistant_response: str):
        """Save conversation to history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversations (user_input, assistant_response)
            VALUES (?, ?)
        """, (user_input, assistant_response))
        
        conn.commit()
        conn.close()
    
    def get_conversation_history(self, limit: int = 10) -> list:
        """Get recent conversation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_input, assistant_response, timestamp
            FROM conversations
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "user": row[0],
                "assistant": row[1],
                "timestamp": row[2]
            }
            for row in reversed(rows)
        ]
    
    def learn_pattern(self, pattern_type: str, pattern_data: Dict):
        """Learn user patterns for personalization"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        pattern_json = json.dumps(pattern_data)
        
        # Check if pattern exists
        cursor.execute("""
            SELECT id, frequency FROM user_patterns
            WHERE pattern_type = ? AND pattern_data = ?
        """, (pattern_type, pattern_json))
        
        row = cursor.fetchone()
        
        if row:
            # Increment frequency
            cursor.execute("""
                UPDATE user_patterns
                SET frequency = frequency + 1, last_seen = ?
                WHERE id = ?
            """, (datetime.now(), row[0]))
        else:
            # Insert new pattern
            cursor.execute("""
                INSERT INTO user_patterns (pattern_type, pattern_data)
                VALUES (?, ?)
            """, (pattern_type, pattern_json))
        
        conn.commit()
        conn.close()
    
    def get_patterns(self, pattern_type: Optional[str] = None) -> list:
        """Get learned patterns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if pattern_type:
            cursor.execute("""
                SELECT pattern_type, pattern_data, frequency, last_seen
                FROM user_patterns
                WHERE pattern_type = ?
                ORDER BY frequency DESC
            """, (pattern_type,))
        else:
            cursor.execute("""
                SELECT pattern_type, pattern_data, frequency, last_seen
                FROM user_patterns
                ORDER BY frequency DESC
            """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "type": row[0],
                "data": json.loads(row[1]),
                "frequency": row[2],
                "last_seen": row[3]
            }
            for row in rows
        ]
    
    def export_profile(self, export_path: Path):
        """Export user profile to JSON"""
        export_data = {
            "user_name": self.user_name,
            "export_date": datetime.now().isoformat(),
            "preferences": {},
            "patterns": self.get_patterns()
        }
        
        # Get all preferences
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM preferences")
        for row in cursor.fetchall():
            export_data["preferences"][row[0]] = json.loads(row[1])
        conn.close()
        
        # Save to file
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"Profile exported to {export_path}")
