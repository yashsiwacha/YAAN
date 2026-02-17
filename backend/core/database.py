"""
YAAN Database Module
SQLite database for user data, learning progress, tasks, and activity tracking
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime, date
from typing import List, Dict, Optional, Any
from contextlib import contextmanager

from core.logger import setup_logger

logger = setup_logger("Database")


class YAANDatabase:
    """SQLite database handler for YAAN"""
    
    def __init__(self, db_path: Optional[Path] = None):
        """Initialize database connection"""
        if db_path is None:
            data_dir = Path(__file__).parent.parent / "data"
            data_dir.mkdir(exist_ok=True)
            db_path = data_dir / "yaan.db"
        
        self.db_path = str(db_path)
        self._init_database()
        logger.info(f"Database initialized at {self.db_path}")
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def _init_database(self):
        """Create database tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Learning Paths table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learning_paths (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    total_problems INTEGER DEFAULT 0,
                    completed_problems INTEGER DEFAULT 0,
                    progress_percent INTEGER DEFAULT 0,
                    color TEXT DEFAULT '#6366f1',
                    icon TEXT DEFAULT '📚',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tasks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    priority TEXT CHECK(priority IN ('low', 'medium', 'high')) DEFAULT 'medium',
                    completed BOOLEAN DEFAULT 0,
                    due_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Activity tracking table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE NOT NULL UNIQUE,
                    level INTEGER DEFAULT 0 CHECK(level >= 0 AND level <= 4),
                    problems_solved INTEGER DEFAULT 0,
                    time_spent_minutes INTEGER DEFAULT 0,
                    streak_day BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # User stats table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stat_key TEXT NOT NULL UNIQUE,
                    stat_value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # LeetCode sync table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS leetcode_sync (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    total_solved INTEGER DEFAULT 0,
                    easy_solved INTEGER DEFAULT 0,
                    medium_solved INTEGER DEFAULT 0,
                    hard_solved INTEGER DEFAULT 0,
                    ranking INTEGER DEFAULT 0,
                    streak INTEGER DEFAULT 0,
                    total_active_days INTEGER DEFAULT 0,
                    topics_json TEXT,
                    last_synced TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            logger.info("Database tables created/verified")
            
            # Insert default data if tables are empty
            self._insert_default_data(conn)
    
    def _insert_default_data(self, conn: sqlite3.Connection):
        """Insert default learning paths and initial data"""
        cursor = conn.cursor()
        
        # Check if learning paths exist
        cursor.execute("SELECT COUNT(*) as count FROM learning_paths")
        count = cursor.fetchone()["count"]
        
        if count == 0:
            logger.info("Inserting default learning paths...")
            default_paths = [
                ("Arrays & Strings", "Data Structures", 50, 32, 65, "#ec4899", "🔢"),
                ("Dynamic Programming", "Algorithms", 40, 16, 40, "#8b5cf6", "🧩"),
                ("Trees & Graphs", "Data Structures", 45, 25, 55, "#10b981", "🌳"),
                ("System Design", "Advanced", 30, 9, 30, "#f59e0b", "🏗️"),
            ]
            
            cursor.executemany("""
                INSERT INTO learning_paths (title, category, total_problems, completed_problems, progress_percent, color, icon)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, default_paths)
            logger.info(f"Inserted {len(default_paths)} learning paths")
        
        # Check if tasks exist
        cursor.execute("SELECT COUNT(*) as count FROM tasks")
        count = cursor.fetchone()["count"]
        
        if count == 0:
            logger.info("Inserting default tasks...")
            from datetime import timedelta
            today = date.today()
            default_tasks = [
                ("Complete Binary Tree problems", "Solve 3 tree traversal problems", "high", 0, (today + timedelta(days=1)).isoformat()),
                ("Review DP patterns", "Go through knapsack and LIS patterns", "medium", 0, (today + timedelta(days=3)).isoformat()),
                ("System Design reading", "Read about load balancers", "low", 0, (today + timedelta(days=7)).isoformat()),
            ]
            
            cursor.executemany("""
                INSERT INTO tasks (title, description, priority, completed, due_date)
                VALUES (?, ?, ?, ?, ?)
            """, default_tasks)
            logger.info(f"Inserted {len(default_tasks)} tasks")
        
        # Initialize user stats
        cursor.execute("SELECT COUNT(*) as count FROM user_stats")
        count = cursor.fetchone()["count"]
        
        if count == 0:
            logger.info("Initializing user stats...")
            stats = [
                ("current_streak", "7"),
                ("longest_streak", "21"),
                ("total_problems_solved", "82"),
                ("total_time_minutes", "2340"),
            ]
            
            cursor.executemany("""
                INSERT INTO user_stats (stat_key, stat_value)
                VALUES (?, ?)
            """, stats)
            logger.info(f"Initialized {len(stats)} user stats")
        
        # Initialize some activity data (last 90 days)
        cursor.execute("SELECT COUNT(*) as count FROM activity")
        count = cursor.fetchone()["count"]
        
        if count == 0:
            logger.info("Generating sample activity data...")
            import random
            from datetime import timedelta
            
            today = date.today()
            activities = []
            
            for i in range(90):
                day = today - timedelta(days=89 - i)
                # Random activity level (0-4)
                level = random.choices([0, 1, 2, 3, 4], weights=[40, 25, 20, 10, 5])[0]
                problems = level * random.randint(1, 3) if level > 0 else 0
                time_spent = problems * random.randint(15, 45) if problems > 0 else 0
                
                activities.append((
                    day.isoformat(),
                    level,
                    problems,
                    time_spent,
                    1 if level > 0 else 0
                ))
            
            cursor.executemany("""
                INSERT INTO activity (date, level, problems_solved, time_spent_minutes, streak_day)
                VALUES (?, ?, ?, ?, ?)
            """, activities)
            logger.info(f"Generated {len(activities)} days of activity data")
    
    # Learning Paths API
    def get_learning_paths(self) -> List[Dict[str, Any]]:
        """Get all learning paths"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, category, total_problems, completed_problems, 
                       progress_percent, color, icon, updated_at
                FROM learning_paths
                ORDER BY id
            """)
            
            paths = []
            for row in cursor.fetchall():
                paths.append({
                    "id": row["id"],
                    "title": row["title"],
                    "category": row["category"],
                    "totalProblems": row["total_problems"],
                    "completedProblems": row["completed_problems"],
                    "progressPercent": row["progress_percent"],
                    "color": row["color"],
                    "icon": row["icon"],
                    "updatedAt": row["updated_at"]
                })
            
            return paths
    
    def update_learning_path_progress(self, path_id: int, completed_problems: int) -> bool:
        """Update progress for a learning path"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get total problems
            cursor.execute("SELECT total_problems FROM learning_paths WHERE id = ?", (path_id,))
            row = cursor.fetchone()
            if not row:
                return False
            
            total = row["total_problems"]
            progress = int((completed_problems / total) * 100) if total > 0 else 0
            
            cursor.execute("""
                UPDATE learning_paths 
                SET completed_problems = ?, progress_percent = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (completed_problems, progress, path_id))
            
            return True
    
    # Tasks API
    def get_tasks(self, include_completed: bool = False) -> List[Dict[str, Any]]:
        """Get all tasks"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if include_completed:
                cursor.execute("""
                    SELECT id, title, description, priority, completed, due_date, created_at
                    FROM tasks
                    ORDER BY completed ASC, due_date ASC
                """)
            else:
                cursor.execute("""
                    SELECT id, title, description, priority, completed, due_date, created_at
                    FROM tasks
                    WHERE completed = 0
                    ORDER BY due_date ASC
                """)
            
            tasks = []
            for row in cursor.fetchall():
                tasks.append({
                    "id": row["id"],
                    "title": row["title"],
                    "description": row["description"],
                    "priority": row["priority"],
                    "completed": bool(row["completed"]),
                    "dueDate": row["due_date"],
                    "createdAt": row["created_at"]
                })
            
            return tasks
    
    def create_task(self, title: str, description: str = "", priority: str = "medium", 
                    due_date: Optional[str] = None) -> int:
        """Create a new task"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (title, description, priority, due_date)
                VALUES (?, ?, ?, ?)
            """, (title, description, priority, due_date))
            
            return cursor.lastrowid
    
    def update_task(self, task_id: int, **kwargs) -> bool:
        """Update a task"""
        valid_fields = ["title", "description", "priority", "completed", "due_date"]
        updates = []
        values = []
        
        for key, value in kwargs.items():
            if key in valid_fields:
                updates.append(f"{key} = ?")
                values.append(value)
        
        if not updates:
            return False
        
        values.append(task_id)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE tasks 
                SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, values)
            
            return cursor.rowcount > 0
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            return cursor.rowcount > 0
    
    # Activity API
    def get_activity(self, days: int = 90) -> List[Dict[str, Any]]:
        """Get activity data for the last N days"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT date, level, problems_solved, time_spent_minutes, streak_day
                FROM activity
                ORDER BY date DESC
                LIMIT ?
            """, (days,))
            
            activities = []
            for row in cursor.fetchall():
                activities.append({
                    "date": row["date"],
                    "level": row["level"],
                    "problemsSolved": row["problems_solved"],
                    "timeSpent": row["time_spent_minutes"],
                    "streakDay": bool(row["streak_day"])
                })
            
            return list(reversed(activities))  # Return oldest to newest
    
    def log_activity(self, activity_date: Optional[str] = None, level: int = 1, 
                     problems_solved: int = 0, time_spent: int = 0) -> bool:
        """Log activity for a date"""
        if activity_date is None:
            activity_date = date.today().isoformat()
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if entry exists for this date
            cursor.execute("SELECT id FROM activity WHERE date = ?", (activity_date,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing entry
                cursor.execute("""
                    UPDATE activity
                    SET level = ?, problems_solved = ?, time_spent_minutes = ?, streak_day = 1
                    WHERE date = ?
                """, (level, problems_solved, time_spent, activity_date))
            else:
                # Insert new entry
                cursor.execute("""
                    INSERT INTO activity (date, level, problems_solved, time_spent_minutes, streak_day)
                    VALUES (?, ?, ?, ?, 1)
                """, (activity_date, level, problems_solved, time_spent))
            
            return True
    
    # User Stats API
    def get_stats(self) -> Dict[str, Any]:
        """Get all user statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT stat_key, stat_value FROM user_stats")
            
            stats = {}
            for row in cursor.fetchall():
                key = row["stat_key"]
                value = row["stat_value"]
                
                # Try to convert to int if possible
                try:
                    stats[key] = int(value)
                except ValueError:
                    stats[key] = value
            
            return stats
    
    def update_stat(self, stat_key: str, stat_value: Any) -> bool:
        """Update a user statistic"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO user_stats (stat_key, stat_value)
                VALUES (?, ?)
                ON CONFLICT(stat_key) 
                DO UPDATE SET stat_value = ?, updated_at = CURRENT_TIMESTAMP
            """, (stat_key, str(stat_value), str(stat_value)))
            
            return True
    
    # LeetCode Sync API
    def save_leetcode_sync(self, sync_data: Dict[str, Any]) -> bool:
        """Save LeetCode sync data"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            username = sync_data.get("username")
            topics_json = json.dumps(sync_data.get("topics", {}))
            
            cursor.execute("""
                INSERT INTO leetcode_sync 
                (username, total_solved, easy_solved, medium_solved, hard_solved, 
                 ranking, streak, total_active_days, topics_json, last_synced)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(username) 
                DO UPDATE SET 
                    total_solved = ?,
                    easy_solved = ?,
                    medium_solved = ?,
                    hard_solved = ?,
                    ranking = ?,
                    streak = ?,
                    total_active_days = ?,
                    topics_json = ?,
                    last_synced = ?
            """, (
                username,
                sync_data.get("totalSolved", 0),
                sync_data.get("easySolved", 0),
                sync_data.get("mediumSolved", 0),
                sync_data.get("hardSolved", 0),
                sync_data.get("ranking", 0),
                sync_data.get("streak", 0),
                sync_data.get("totalActiveDays", 0),
                topics_json,
                sync_data.get("lastSynced"),
                # For UPDATE clause
                sync_data.get("totalSolved", 0),
                sync_data.get("easySolved", 0),
                sync_data.get("mediumSolved", 0),
                sync_data.get("hardSolved", 0),
                sync_data.get("ranking", 0),
                sync_data.get("streak", 0),
                sync_data.get("totalActiveDays", 0),
                topics_json,
                sync_data.get("lastSynced")
            ))
            
            logger.info(f"LeetCode sync saved for {username}")
            return True
    
    def get_leetcode_sync(self, username: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get LeetCode sync data"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if username:
                cursor.execute("""
                    SELECT * FROM leetcode_sync WHERE username = ?
                """, (username,))
            else:
                # Get most recent sync
                cursor.execute("""
                    SELECT * FROM leetcode_sync ORDER BY last_synced DESC LIMIT 1
                """)
            
            row = cursor.fetchone()
            if not row:
                return None
            
            topics = {}
            if row["topics_json"]:
                try:
                    topics = json.loads(row["topics_json"])
                except:
                    pass
            
            return {
                "username": row["username"],
                "totalSolved": row["total_solved"],
                "easySolved": row["easy_solved"],
                "mediumSolved": row["medium_solved"],
                "hardSolved": row["hard_solved"],
                "ranking": row["ranking"],
                "streak": row["streak"],
                "totalActiveDays": row["total_active_days"],
                "topics": topics,
                "lastSynced": row["last_synced"]
            }
    
    def update_learning_paths_from_leetcode(self, sync_data: Dict[str, Any]) -> bool:
        """Update learning paths with LeetCode data"""
        from core.leetcode import map_topics_to_learning_paths
        
        topics = sync_data.get("topics", {})
        path_counts = map_topics_to_learning_paths(topics)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            for path_title, completed in path_counts.items():
                # Get current path data
                cursor.execute("""
                    SELECT id, total_problems FROM learning_paths 
                    WHERE title = ?
                """, (path_title,))
                
                row = cursor.fetchone()
                if row:
                    path_id = row["id"]
                    total = row["total_problems"]
                    
                    # Use completed count, but don't exceed total
                    completed = min(completed, total)
                    progress = int((completed / total) * 100) if total > 0 else 0
                    
                    cursor.execute("""
                        UPDATE learning_paths 
                        SET completed_problems = ?, 
                            progress_percent = ?, 
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (completed, progress, path_id))
            
            logger.info("Learning paths updated from LeetCode data")
            return True
