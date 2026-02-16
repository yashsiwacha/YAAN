"""
Proactive Learning System - AI asks questions to learn about users
"""

import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
import sqlite3

from core.logger import setup_logger

logger = setup_logger("ProactiveLearning")


class ProactiveLearning:
    """System for AI to ask questions and learn about users proactively"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_database()
        
        # Question categories and templates
        self.question_templates = {
            "personal": [
                "What do you do for work?",
                "What are your hobbies or interests?",
                "What programming languages do you work with most?",
                "What's your favorite type of project to work on?",
                "What tools do you use daily?",
            ],
            "preferences": [
                "Do you prefer detailed explanations or concise answers?",
                "What time of day do you usually work on coding projects?",
                "How would you like me to format code explanations?",
                "Would you like me to be more formal or casual?",
                "Do you prefer emojis in responses or plain text?",
            ],
            "goals": [
                "What are you currently learning or working towards?",
                "What skills would you like to improve?",
                "Are there any topics you'd like me to help you with regularly?",
                "What's your biggest challenge right now?",
                "What would make me more helpful to you?",
            ],
            "workflow": [
                "What's your typical daily routine?",
                "When do you prefer to receive reminders?",
                "How do you organize your tasks?",
                "What helps you stay productive?",
                "Do you have any regular meetings or commitments?",
            ],
            "feedback": [
                "How am I doing so far?",
                "Is there anything I should do differently?",
                "What features do you use most?",
                "What would you like me to improve?",
                "Am I asking too many questions?",
            ]
        }
        
        logger.info("Proactive learning system initialized")
    
    def _init_database(self):
        """Initialize the learning database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Questions asked history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS asked_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                question TEXT NOT NULL,
                asked_at TIMESTAMP NOT NULL,
                answered BOOLEAN DEFAULT FALSE,
                answer TEXT,
                answered_at TIMESTAMP
            )
        """)
        
        # Learning settings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        
        # Initialize default settings
        cursor.execute("""
            INSERT OR IGNORE INTO learning_settings (key, value)
            VALUES ('questions_enabled', 'true')
        """)
        cursor.execute("""
            INSERT OR IGNORE INTO learning_settings (key, value)
            VALUES ('questions_per_session', '2')
        """)
        cursor.execute("""
            INSERT OR IGNORE INTO learning_settings (key, value)
            VALUES ('min_messages_before_question', '5')
        """)
        cursor.execute("""
            INSERT OR IGNORE INTO learning_settings (key, value)
            VALUES ('last_question_time', '1970-01-01 00:00:00')
        """)
        
        conn.commit()
        conn.close()
        logger.info("Learning database initialized")
    
    def should_ask_question(self, message_count: int) -> bool:
        """Determine if AI should ask a question now"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if questions are enabled
        cursor.execute("SELECT value FROM learning_settings WHERE key = 'questions_enabled'")
        enabled = cursor.fetchone()[0] == 'true'
        
        if not enabled:
            conn.close()
            return False
        
        # Check minimum messages threshold
        cursor.execute("SELECT value FROM learning_settings WHERE key = 'min_messages_before_question'")
        min_messages = int(cursor.fetchone()[0])
        
        if message_count < min_messages:
            conn.close()
            return False
        
        # Check last question time (don't ask too frequently)
        cursor.execute("SELECT value FROM learning_settings WHERE key = 'last_question_time'")
        last_time_str = cursor.fetchone()[0]
        last_time = datetime.fromisoformat(last_time_str)
        
        # Wait at least 10 messages or 5 minutes before asking another question
        time_diff = datetime.now() - last_time
        if time_diff < timedelta(minutes=5):
            conn.close()
            return False
        
        # Check how many questions asked today
        today = datetime.now().date()
        cursor.execute("""
            SELECT COUNT(*) FROM asked_questions 
            WHERE DATE(asked_at) = ?
        """, (today,))
        questions_today = cursor.fetchone()[0]
        
        cursor.execute("SELECT value FROM learning_settings WHERE key = 'questions_per_session'")
        max_per_session = int(cursor.fetchone()[0])
        
        conn.close()
        
        if questions_today >= max_per_session:
            return False
        
        # Random probability to make it feel natural (30% chance when conditions met)
        return random.random() < 0.3
    
    def get_next_question(self) -> Optional[Dict[str, str]]:
        """Get the next appropriate question to ask"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get questions already asked
        cursor.execute("SELECT question FROM asked_questions")
        asked = {row[0] for row in cursor.fetchall()}
        
        # Find categories with fewest questions answered
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM asked_questions
            WHERE answered = TRUE
            GROUP BY category
            ORDER BY count ASC
        """)
        category_counts = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Choose category with least answered questions
        all_categories = list(self.question_templates.keys())
        category = min(all_categories, key=lambda c: category_counts.get(c, 0))
        
        # Find unasked question in that category
        available_questions = [
            q for q in self.question_templates[category]
            if q not in asked
        ]
        
        if not available_questions:
            # All questions in this category asked, try another
            for cat in all_categories:
                available_questions = [
                    q for q in self.question_templates[cat]
                    if q not in asked
                ]
                if available_questions:
                    category = cat
                    break
        
        if not available_questions:
            conn.close()
            return None
        
        question = random.choice(available_questions)
        
        # Record that we're asking this question
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO asked_questions (category, question, asked_at)
            VALUES (?, ?, ?)
        """, (category, question, now))
        
        # Update last question time
        cursor.execute("""
            UPDATE learning_settings
            SET value = ?
            WHERE key = 'last_question_time'
        """, (now,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Generated question from category '{category}': {question}")
        
        return {
            "category": category,
            "question": question,
            "formatted": f"💭 By the way, I'm curious: {question}"
        }
    
    def record_answer(self, question: str, answer: str):
        """Record user's answer to a question"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        cursor.execute("""
            UPDATE asked_questions
            SET answered = TRUE,
                answer = ?,
                answered_at = ?
            WHERE question = ?
            AND answered = FALSE
        """, (answer, now, question))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Recorded answer to question: {question[:50]}...")
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of learning progress"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total questions asked
        cursor.execute("SELECT COUNT(*) FROM asked_questions")
        total_asked = cursor.fetchone()[0]
        
        # Questions answered
        cursor.execute("SELECT COUNT(*) FROM asked_questions WHERE answered = TRUE")
        total_answered = cursor.fetchone()[0]
        
        # By category
        cursor.execute("""
            SELECT category, COUNT(*) as total,
                   SUM(CASE WHEN answered THEN 1 ELSE 0 END) as answered
            FROM asked_questions
            GROUP BY category
        """)
        categories = {
            row[0]: {"asked": row[1], "answered": row[2]}
            for row in cursor.fetchall()
        }
        
        conn.close()
        
        return {
            "total_asked": total_asked,
            "total_answered": total_answered,
            "answer_rate": (total_answered / total_asked * 100) if total_asked > 0 else 0,
            "categories": categories
        }
    
    def toggle_questions(self, enabled: bool):
        """Enable or disable proactive questions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE learning_settings
            SET value = ?
            WHERE key = 'questions_enabled'
        """, ('true' if enabled else 'false',))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Proactive questions {'enabled' if enabled else 'disabled'}")
    
    def set_questions_per_session(self, count: int):
        """Set maximum questions per session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE learning_settings
            SET value = ?
            WHERE key = 'questions_per_session'
        """, (str(count),))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Questions per session set to {count}")
    
    def get_recent_questions(self, limit: int = 10) -> list:
        """Get recently asked questions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT question, category, asked_at, answered, answer
            FROM asked_questions
            ORDER BY asked_at DESC
            LIMIT ?
        """, (limit,))
        
        questions = []
        for row in cursor.fetchall():
            questions.append({
                "question": row[0],
                "category": row[1],
                "asked_at": row[2],
                "answered": bool(row[3]),
                "answer": row[4]
            })
        
        conn.close()
        return questions
