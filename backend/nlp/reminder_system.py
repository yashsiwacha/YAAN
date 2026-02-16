"""
Reminder and Todo Management System
Helps users create, manage, and track reminders and tasks
"""

import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import re

from core.logger import setup_logger

logger = setup_logger("ReminderSystem")


class ReminderSystem:
    """Manage reminders and todo lists"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database for reminders and todos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Reminders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                due_time TEXT,
                priority TEXT DEFAULT 'medium',
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                recurring TEXT
            )
        """)
        
        # Todos table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT DEFAULT 'medium',
                status TEXT DEFAULT 'pending',
                category TEXT,
                due_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)
        
        # Tags table for categorization
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                todo_id INTEGER,
                tag TEXT,
                FOREIGN KEY (todo_id) REFERENCES todos(id)
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Reminder system database initialized")
    
    def create_reminder(self, title: str, description: str = "", 
                       due_date: Optional[str] = None, due_time: Optional[str] = None,
                       priority: str = "medium") -> int:
        """Create a new reminder"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO reminders (title, description, due_date, due_time, priority)
            VALUES (?, ?, ?, ?, ?)
        """, (title, description, due_date, due_time, priority))
        
        reminder_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Created reminder: {title} (ID: {reminder_id})")
        return reminder_id
    
    def create_todo(self, title: str, description: str = "",
                   priority: str = "medium", category: str = "",
                   due_date: Optional[str] = None, tags: List[str] = None) -> int:
        """Create a new todo item"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO todos (title, description, priority, category, due_date)
            VALUES (?, ?, ?, ?, ?)
        """, (title, description, priority, category, due_date))
        
        todo_id = cursor.lastrowid
        
        # Add tags if provided
        if tags:
            for tag in tags:
                cursor.execute("""
                    INSERT INTO tags (todo_id, tag)
                    VALUES (?, ?)
                """, (todo_id, tag.strip()))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Created todo: {title} (ID: {todo_id})")
        return todo_id
    
    def get_reminders(self, status: str = "all") -> List[Dict[str, Any]]:
        """Get reminders, optionally filtered by status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status == "all":
            cursor.execute("""
                SELECT id, title, description, due_date, due_time, priority, status, created_at
                FROM reminders
                ORDER BY 
                    CASE priority 
                        WHEN 'high' THEN 1 
                        WHEN 'medium' THEN 2 
                        WHEN 'low' THEN 3 
                    END,
                    due_date ASC NULLS LAST
            """)
        else:
            cursor.execute("""
                SELECT id, title, description, due_date, due_time, priority, status, created_at
                FROM reminders
                WHERE status = ?
                ORDER BY 
                    CASE priority 
                        WHEN 'high' THEN 1 
                        WHEN 'medium' THEN 2 
                        WHEN 'low' THEN 3 
                    END,
                    due_date ASC NULLS LAST
            """, (status,))
        
        rows = cursor.fetchall()
        conn.close()
        
        reminders = []
        for row in rows:
            reminders.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "due_date": row[3],
                "due_time": row[4],
                "priority": row[5],
                "status": row[6],
                "created_at": row[7]
            })
        
        return reminders
    
    def get_todos(self, status: str = "all", category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get todos, optionally filtered by status and category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT id, title, description, priority, status, category, due_date, created_at
            FROM todos
            WHERE 1=1
        """
        params = []
        
        if status != "all":
            query += " AND status = ?"
            params.append(status)
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += """
            ORDER BY 
                CASE priority 
                    WHEN 'high' THEN 1 
                    WHEN 'medium' THEN 2 
                    WHEN 'low' THEN 3 
                END,
                due_date ASC NULLS LAST
        """
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Get tags for each todo
        todos = []
        for row in rows:
            todo_id = row[0]
            cursor.execute("SELECT tag FROM tags WHERE todo_id = ?", (todo_id,))
            tags = [tag_row[0] for tag_row in cursor.fetchall()]
            
            todos.append({
                "id": todo_id,
                "title": row[1],
                "description": row[2],
                "priority": row[3],
                "status": row[4],
                "category": row[5],
                "due_date": row[6],
                "created_at": row[7],
                "tags": tags
            })
        
        conn.close()
        return todos
    
    def complete_reminder(self, reminder_id: int) -> bool:
        """Mark a reminder as completed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE reminders
            SET status = 'completed', completed_at = ?
            WHERE id = ?
        """, (datetime.now(), reminder_id))
        
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        if affected > 0:
            logger.info(f"Completed reminder ID: {reminder_id}")
            return True
        return False
    
    def complete_todo(self, todo_id: int) -> bool:
        """Mark a todo as completed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE todos
            SET status = 'completed', completed_at = ?
            WHERE id = ?
        """, (datetime.now(), todo_id))
        
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        if affected > 0:
            logger.info(f"Completed todo ID: {todo_id}")
            return True
        return False
    
    def delete_reminder(self, reminder_id: int) -> bool:
        """Delete a reminder"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        if affected > 0:
            logger.info(f"Deleted reminder ID: {reminder_id}")
            return True
        return False
    
    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete associated tags
        cursor.execute("DELETE FROM tags WHERE todo_id = ?", (todo_id,))
        
        # Delete todo
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        if affected > 0:
            logger.info(f"Deleted todo ID: {todo_id}")
            return True
        return False
    
    def parse_reminder_from_text(self, text: str) -> Dict[str, Any]:
        """Parse reminder details from natural language"""
        result = {
            "title": "",
            "description": "",
            "due_date": None,
            "due_time": None,
            "priority": "medium"
        }
        
        # Extract priority
        if re.search(r'\b(urgent|important|high priority)\b', text, re.IGNORECASE):
            result["priority"] = "high"
        elif re.search(r'\b(low priority|not urgent)\b', text, re.IGNORECASE):
            result["priority"] = "low"
        
        # Extract time patterns
        time_patterns = {
            "tomorrow": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "today": datetime.now().strftime("%Y-%m-%d"),
            "next week": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        }
        
        for pattern, date in time_patterns.items():
            if pattern in text.lower():
                result["due_date"] = date
                break
        
        # Extract specific time
        time_match = re.search(r'at (\d{1,2}):?(\d{2})?\s*(am|pm)?', text, re.IGNORECASE)
        if time_match:
            hour = int(time_match.group(1))
            minute = time_match.group(2) or "00"
            ampm = time_match.group(3) or ""
            
            if ampm.lower() == "pm" and hour < 12:
                hour += 12
            elif ampm.lower() == "am" and hour == 12:
                hour = 0
            
            result["due_time"] = f"{hour:02d}:{minute}"
        
        # Extract title (after "remind me to" or similar)
        title_match = re.search(r'remind me (?:to|about) (.+?)(?:\s+(?:tomorrow|today|at|on|next)|$)', text, re.IGNORECASE)
        if title_match:
            result["title"] = title_match.group(1).strip()
        else:
            # Fallback: use everything after "remind"
            fallback_match = re.search(r'remind me (.+)', text, re.IGNORECASE)
            if fallback_match:
                result["title"] = fallback_match.group(1).strip()
        
        return result
    
    def parse_todo_from_text(self, text: str) -> Dict[str, Any]:
        """Parse todo details from natural language"""
        result = {
            "title": "",
            "description": "",
            "priority": "medium",
            "category": "",
            "tags": []
        }
        
        # Extract priority
        if re.search(r'\b(urgent|important|high priority)\b', text, re.IGNORECASE):
            result["priority"] = "high"
        elif re.search(r'\b(low priority|not urgent)\b', text, re.IGNORECASE):
            result["priority"] = "low"
        
        # Extract category
        category_match = re.search(r'category:?\s*(\w+)', text, re.IGNORECASE)
        if category_match:
            result["category"] = category_match.group(1)
        
        # Extract tags
        tag_matches = re.findall(r'#(\w+)', text)
        if tag_matches:
            result["tags"] = tag_matches
        
        # Extract title
        title_match = re.search(r'(?:add|create|make)(?: a| an)? (?:todo|task):?\s*(.+?)(?:\s+category:|$)', text, re.IGNORECASE)
        if title_match:
            result["title"] = title_match.group(1).strip()
            # Remove tags from title
            result["title"] = re.sub(r'#\w+', '', result["title"]).strip()
        else:
            # Fallback
            fallback_match = re.search(r'(?:todo|task):?\s*(.+)', text, re.IGNORECASE)
            if fallback_match:
                result["title"] = fallback_match.group(1).strip()
                result["title"] = re.sub(r'#\w+', '', result["title"]).strip()
        
        return result
    
    def format_reminders_list(self, reminders: List[Dict[str, Any]]) -> str:
        """Format reminders for display"""
        if not reminders:
            return "You have no reminders. Create one by saying 'Remind me to...'"
        
        output = "**Your Reminders:**\n\n"
        
        for reminder in reminders:
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            emoji = priority_emoji.get(reminder["priority"], "⚪")
            status_emoji = "✅" if reminder["status"] == "completed" else "⏰"
            
            output += f"{status_emoji} {emoji} **[{reminder['id']}]** {reminder['title']}\n"
            
            if reminder["due_date"]:
                output += f"   📅 Due: {reminder['due_date']}"
                if reminder["due_time"]:
                    output += f" at {reminder['due_time']}"
                output += "\n"
            
            if reminder["description"]:
                output += f"   📝 {reminder['description']}\n"
            
            output += "\n"
        
        return output
    
    def format_todos_list(self, todos: List[Dict[str, Any]]) -> str:
        """Format todos for display"""
        if not todos:
            return "You have no todos. Create one by saying 'Add todo...'"
        
        output = "**Your Todos:**\n\n"
        
        for todo in todos:
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            emoji = priority_emoji.get(todo["priority"], "⚪")
            status_emoji = "☑️" if todo["status"] == "completed" else "☐"
            
            output += f"{status_emoji} {emoji} **[{todo['id']}]** {todo['title']}\n"
            
            if todo["category"]:
                output += f"   📂 Category: {todo['category']}\n"
            
            if todo["tags"]:
                output += f"   🏷️ Tags: {', '.join(todo['tags'])}\n"
            
            if todo["due_date"]:
                output += f"   📅 Due: {todo['due_date']}\n"
            
            if todo["description"]:
                output += f"   📝 {todo['description']}\n"
            
            output += "\n"
        
        return output
    
    def get_summary(self) -> str:
        """Get a summary of all reminders and todos"""
        pending_reminders = len(self.get_reminders("pending"))
        completed_reminders = len(self.get_reminders("completed"))
        pending_todos = len(self.get_todos("pending"))
        completed_todos = len(self.get_todos("completed"))
        
        summary = f"""**Task Summary:**

⏰ Reminders: {pending_reminders} pending, {completed_reminders} completed
☐ Todos: {pending_todos} pending, {completed_todos} completed

Type 'show reminders' or 'show todos' to see details."""
        
        return summary
