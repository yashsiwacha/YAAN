"""
YAAN FastAPI Server
Handles REST API and WebSocket connections
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List
import uvicorn

from core.config import YAANConfig
from core.logger import setup_logger
from core.database import YAANDatabase
from core.leetcode import LeetCodeAPI
# Voice modules will be lazy-loaded
# from voice.speech_recognition import SpeechRecognizer
# from voice.text_to_speech import TextToSpeech
from nlp.command_processor import CommandProcessor

logger = setup_logger("Server")


class YAANServer:
    """Main YAAN server handling all client connections"""
    
    def __init__(self, config: YAANConfig):
        self.config = config
        self.app = FastAPI(
            title="YAAN Backend",
            description="Your AI Assistant Network API",
            version="0.1.0"
        )
        
        # Active WebSocket connections
        self.active_connections: List[WebSocket] = []
        
        # Initialize components
        self._init_components()
        self._setup_routes()
        self._setup_middleware()
        self._setup_static_files()
    
    def _init_components(self):
        """Initialize AI components"""
        logger.info("Initializing AI components...")
        
        try:
            # Database
            self.database = YAANDatabase()
            
            # LeetCode API
            self.leetcode_api = LeetCodeAPI()
            
            # Speech recognition (will be lazy-loaded)
            self.speech_recognizer = None  # SpeechRecognizer(self.config.ai)
            
            # Text to speech
            self.tts = None  # TextToSpeech(self.config.voice)
            
            # Command processor
            self.command_processor = CommandProcessor(self.config)
            
            logger.info("Components initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            raise
    
    def _setup_middleware(self):
        """Setup middleware for CORS, etc."""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # For development
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def _setup_static_files(self):
        """Setup static file serving for web UI"""
        static_dir = Path(__file__).parent.parent / "static"
        if static_dir.exists():
            self.app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/")
        async def root():
            """Serve web UI"""
            static_dir = Path(__file__).parent.parent / "static"
            index_file = static_dir / "index.html"
            if index_file.exists():
                return FileResponse(index_file)
            else:
                return {
                    "status": "online",
                    "service": "YAAN",
                    "version": "0.1.0",
                    "user": self.config.user.name,
                    "message": "Web UI not found. Use /api/status for API status."
                }
        
        @self.app.get("/api/status")
        async def get_status():
            """Get system status"""
            return {
                "status": "online",
                "service": "YAAN",
                "version": "0.1.0",
                "user": self.config.user.name,
                "connections": len(self.active_connections),
                "components": {
                    "speech_recognition": self.speech_recognizer is not None,
                    "tts": self.tts is not None,
                    "command_processor": True
                }
            }
        
        @self.app.post("/api/command")
        async def process_command(text: str):
            """Process text command"""
            try:
                response = await self.command_processor.process(text)
                return {"success": True, "response": response}
            except Exception as e:
                logger.error(f"Command processing error: {e}")
                return {"success": False, "error": str(e)}
        
        # Learning Paths API
        @self.app.get("/api/learning-paths")
        async def get_learning_paths():
            """Get all learning paths"""
            try:
                paths = self.database.get_learning_paths()
                return {"success": True, "data": paths}
            except Exception as e:
                logger.error(f"Error fetching learning paths: {e}")
                return {"success": False, "error": str(e)}
        
        @self.app.put("/api/learning-paths/{path_id}")
        async def update_learning_path(path_id: int, completed_problems: int):
            """Update learning path progress"""
            try:
                success = self.database.update_learning_path_progress(path_id, completed_problems)
                if success:
                    return {"success": True, "message": "Progress updated"}
                else:
                    return {"success": False, "error": "Path not found"}
            except Exception as e:
                logger.error(f"Error updating learning path: {e}")
                return {"success": False, "error": str(e)}
        
        # Tasks API
        @self.app.get("/api/tasks")
        async def get_tasks(include_completed: bool = False):
            """Get all tasks"""
            try:
                tasks = self.database.get_tasks(include_completed)
                return {"success": True, "data": tasks}
            except Exception as e:
                logger.error(f"Error fetching tasks: {e}")
                return {"success": False, "error": str(e)}
        
        @self.app.post("/api/tasks")
        async def create_task(title: str, description: str = "", priority: str = "medium", due_date: str = None):
            """Create a new task"""
            try:
                task_id = self.database.create_task(title, description, priority, due_date)
                return {"success": True, "data": {"id": task_id}}
            except Exception as e:
                logger.error(f"Error creating task: {e}")
                return {"success": False, "error": str(e)}
        
        @self.app.put("/api/tasks/{task_id}")
        async def update_task(task_id: int, title: str = None, description: str = None, 
                            priority: str = None, completed: bool = None, due_date: str = None):
            """Update a task"""
            try:
                updates = {}
                if title is not None:
                    updates["title"] = title
                if description is not None:
                    updates["description"] = description
                if priority is not None:
                    updates["priority"] = priority
                if completed is not None:
                    updates["completed"] = 1 if completed else 0
                if due_date is not None:
                    updates["due_date"] = due_date
                
                success = self.database.update_task(task_id, **updates)
                if success:
                    return {"success": True, "message": "Task updated"}
                else:
                    return {"success": False, "error": "Task not found"}
            except Exception as e:
                logger.error(f"Error updating task: {e}")
                return {"success": False, "error": str(e)}
        
        @self.app.delete("/api/tasks/{task_id}")
        async def delete_task(task_id: int):
            """Delete a task"""
            try:
                success = self.database.delete_task(task_id)
                if success:
                    return {"success": True, "message": "Task deleted"}
                else:
                    return {"success": False, "error": "Task not found"}
            except Exception as e:
                logger.error(f"Error deleting task: {e}")
                return {"success": False, "error": str(e)}
        
        # Activity API
        @self.app.get("/api/activity")
        async def get_activity(days: int = 90):
            """Get activity data for last N days"""
            try:
                activity = self.database.get_activity(days)
                return {"success": True, "data": activity}
            except Exception as e:
                logger.error(f"Error fetching activity: {e}")
                return {"success": False, "error": str(e)}
        
        @self.app.post("/api/activity")
        async def log_activity(date: str = None, level: int = 1, 
                              problems_solved: int = 0, time_spent: int = 0):
            """Log activity for a date"""
            try:
                success = self.database.log_activity(date, level, problems_solved, time_spent)
                return {"success": True, "message": "Activity logged"}
            except Exception as e:
                logger.error(f"Error logging activity: {e}")
                return {"success": False, "error": str(e)}
        
        # User Stats API
        @self.app.get("/api/stats")
        async def get_stats():
            """Get user statistics"""
            try:
                stats = self.database.get_stats()
                return {"success": True, "data": stats}
            except Exception as e:
                logger.error(f"Error fetching stats: {e}")
                return {"success": False, "error": str(e)}
        
        # LeetCode Sync API
        @self.app.post("/api/leetcode/sync")
        async def sync_leetcode(username: str):
            """Sync data from LeetCode account"""
            try:
                logger.info(f"Starting LeetCode sync for: {username}")
                
                # Fetch data from LeetCode
                sync_data = self.leetcode_api.sync_user_data(username)
                
                if not sync_data:
                    return {"success": False, "error": "Failed to fetch LeetCode data. Check username."}
                
                # Save to database
                self.database.save_leetcode_sync(sync_data)
                
                # Update learning paths
                self.database.update_learning_paths_from_leetcode(sync_data)
                
                # Update stats
                self.database.update_stat("current_streak", sync_data.get("streak", 0))
                self.database.update_stat("total_problems_solved", sync_data.get("totalSolved", 0))
                
                return {"success": True, "data": sync_data, "message": "LeetCode sync completed"}
            except Exception as e:
                logger.error(f"Error syncing LeetCode: {e}")
                return {"success": False, "error": str(e)}
        
        @self.app.get("/api/leetcode/status")
        async def get_leetcode_status():
            """Get LeetCode sync status"""
            try:
                sync_data = self.database.get_leetcode_sync()
                if sync_data:
                    return {"success": True, "data": sync_data}
                else:
                    return {"success": True, "data": None, "message": "No LeetCode account linked"}
            except Exception as e:
                logger.error(f"Error fetching LeetCode status: {e}")
                return {"success": False, "error": str(e)}
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time communication"""
            await self.handle_websocket(websocket)
    
    async def handle_websocket(self, websocket: WebSocket):
        """Handle WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Active connections: {len(self.active_connections)}")
        
        try:
            await websocket.send_json({
                "type": "welcome",
                "message": f"Hello! I'm YAAN, your AI assistant. How can I help you today?"
            })
            
            while True:
                # Receive message from client
                data = await websocket.receive_json()
                
                # Process command
                if data.get("type") == "command":
                    text = data.get("text", "")
                    response = await self.command_processor.process(text)
                    
                    await websocket.send_json({
                        "type": "response",
                        "text": response
                    })
                
        except WebSocketDisconnect:
            self.active_connections.remove(websocket)
            logger.info(f"Client disconnected. Active connections: {len(self.active_connections)}")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
    
    async def start(self):
        """Start the server"""
        logger.info(f"Starting server on {self.config.server.host}:{self.config.server.port}")
        
        config = uvicorn.Config(
            self.app,
            host=self.config.server.host,
            port=self.config.server.port,
            log_level="info" if self.config.server.debug else "warning"
        )
        
        server = uvicorn.Server(config)
        await server.serve()


# Create a module-level app instance for uvicorn to pick up
from core.config import load_config
_config = load_config()
_server = YAANServer(_config)
app = _server.app
