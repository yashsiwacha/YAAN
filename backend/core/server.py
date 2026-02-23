"""
YAAN FastAPI Server
Handles REST API and WebSocket connections
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import uvicorn
from pydantic import BaseModel, Field

from core.config import YAANConfig
from core.logger import setup_logger
from core.database import YAANDatabase
from core.leetcode import LeetCodeAPI
from core.auth import AuthManager
# Voice modules will be lazy-loaded
# from voice.speech_recognition import SpeechRecognizer
# from voice.text_to_speech import TextToSpeech
from nlp.command_processor import CommandProcessor

logger = setup_logger("Server")


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=200)
    email: Optional[str] = None


class LoginRequest(BaseModel):
    identifier: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=6, max_length=200)


class LeetCodeLoginRequest(BaseModel):
    username: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=6, max_length=200)


class LeetCodeLinkRequest(BaseModel):
    username: str = Field(min_length=2, max_length=100)
    auto_sync: bool = True


class YAANServer:
    """Main YAAN server handling all client connections"""
    
    def __init__(self, config: YAANConfig):
        self.config = config
        project_root = Path(__file__).resolve().parents[2]
        self.legacy_static_dir = Path(__file__).parent.parent / "static"
        desktop_dist_dir = project_root / "desktop" / "dist"
        desktop_index_file = desktop_dist_dir / "index.html"
        self.web_ui_dir = desktop_dist_dir if desktop_index_file.exists() else self.legacy_static_dir
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

            # Auth manager
            self.auth_manager = AuthManager()
            
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
        if self.web_ui_dir.exists():
            self.app.mount("/static", StaticFiles(directory=str(self.web_ui_dir)), name="static")

    @staticmethod
    def _extract_bearer_token(authorization: Optional[str]) -> Optional[str]:
        """Extract bearer token from Authorization header"""
        if not authorization:
            return None
        prefix = "bearer "
        value = authorization.strip()
        if value.lower().startswith(prefix):
            return value[len(prefix):].strip()
        return None

    def _get_current_user(self, authorization: Optional[str]) -> Optional[Dict[str, Any]]:
        """Resolve current user from bearer token"""
        token = self._extract_bearer_token(authorization)
        if not token:
            return None
        return self.database.get_user_by_session_token(token)

    def _create_session_for_user(self, user_id: int) -> str:
        """Create auth session and return raw token"""
        token = self.auth_manager.generate_session_token()
        expires_at = self.auth_manager.default_session_expiry()
        self.database.create_session(user_id, token, expires_at)
        self.database.update_last_login(user_id)
        return token

    def _user_payload(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize user response payload"""
        return {
            "id": user.get("id"),
            "username": user.get("username"),
            "email": user.get("email"),
            "authProvider": user.get("authProvider"),
            "leetcodeUsername": user.get("leetcodeUsername"),
            "createdAt": user.get("createdAt"),
            "lastLoginAt": user.get("lastLoginAt"),
        }

    def _create_unique_username(self, base_username: str) -> str:
        """Generate unique username if base is taken"""
        candidate = base_username.strip()
        if not candidate:
            candidate = "user"

        if not self.database.username_exists(candidate):
            return candidate

        suffix = 1
        while True:
            trial = f"{candidate}{suffix}"
            if not self.database.username_exists(trial):
                return trial
            suffix += 1

    def _sync_leetcode_for_user(self, username: str, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Sync LeetCode account and persist YAAN progress updates"""
        sync_data = self.leetcode_api.sync_user_data(username)
        if not sync_data:
            raise HTTPException(status_code=404, detail="Failed to fetch LeetCode data. Check username.")

        self.database.save_leetcode_sync(sync_data)
        self.database.update_learning_paths_from_leetcode(sync_data)
        self.database.update_stat("current_streak", sync_data.get("streak", 0))
        self.database.update_stat("total_problems_solved", sync_data.get("totalSolved", 0))

        if user_id is not None:
            self.database.link_leetcode_account(user_id, username)
            self.database.mark_leetcode_sync(user_id)

        return sync_data
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/")
        async def root():
            """Serve web UI"""
            index_file = self.web_ui_dir / "index.html"
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

        @self.app.post("/api/auth/register")
        async def register(payload: RegisterRequest):
            """Register a local YAAN user"""
            if self.database.username_exists(payload.username):
                raise HTTPException(status_code=409, detail="Username already exists")

            if payload.email and self.database.email_exists(payload.email):
                raise HTTPException(status_code=409, detail="Email already exists")

            password_hash = self.auth_manager.hash_password(payload.password)
            user = self.database.create_user(
                username=payload.username,
                email=payload.email,
                password_hash=password_hash,
                auth_provider="local",
            )

            token = self._create_session_for_user(user["id"])
            return {"success": True, "data": {"token": token, "user": self._user_payload(user)}}

        @self.app.post("/api/auth/login")
        async def login(payload: LoginRequest):
            """Login with username/email and password"""
            user_record = self.database.get_user_auth_record(payload.identifier)
            if not user_record or not user_record.get("passwordHash"):
                raise HTTPException(status_code=401, detail="Invalid credentials")

            if not self.auth_manager.verify_password(payload.password, user_record["passwordHash"]):
                raise HTTPException(status_code=401, detail="Invalid credentials")

            token = self._create_session_for_user(user_record["id"])
            return {"success": True, "data": {"token": token, "user": self._user_payload(user_record)}}

        @self.app.post("/api/auth/login/leetcode")
        async def login_with_leetcode(payload: LeetCodeLoginRequest):
            """Login with LeetCode username + password (YAAN credential bound to LeetCode username)"""
            profile = self.leetcode_api.get_user_profile(payload.username)
            if not profile:
                raise HTTPException(status_code=404, detail="LeetCode user not found")

            linked_user = self.database.get_user_by_leetcode_username(payload.username)
            if linked_user:
                user_record = self.database.get_user_auth_record(linked_user["username"])
                password_hash = user_record.get("passwordHash") if user_record else None

                if password_hash:
                    if not self.auth_manager.verify_password(payload.password, password_hash):
                        raise HTTPException(status_code=401, detail="Invalid credentials")
                    user = user_record
                else:
                    new_hash = self.auth_manager.hash_password(payload.password)
                    self.database.set_user_password_hash(linked_user["id"], new_hash, auth_provider="leetcode")
                    user = self.database.get_user_by_id(linked_user["id"])
            else:
                generated_username = self._create_unique_username(payload.username)
                password_hash = self.auth_manager.hash_password(payload.password)
                user = self.database.create_user(
                    username=generated_username,
                    email=None,
                    password_hash=password_hash,
                    auth_provider="leetcode",
                    leetcode_username=payload.username,
                )

            self.database.link_leetcode_account(user["id"], payload.username)
            sync_data = self._sync_leetcode_for_user(payload.username, user["id"])
            token = self._create_session_for_user(user["id"])

            return {
                "success": True,
                "data": {
                    "token": token,
                    "user": self._user_payload(user),
                    "leetcodeSync": sync_data,
                },
            }

        @self.app.post("/api/auth/logout")
        async def logout(authorization: Optional[str] = Header(default=None)):
            """Logout current session"""
            token = self._extract_bearer_token(authorization)
            if token:
                self.database.revoke_session(token)
            return {"success": True, "message": "Logged out"}

        @self.app.get("/api/auth/me")
        async def get_current_user(authorization: Optional[str] = Header(default=None)):
            """Get currently authenticated user"""
            user = self._get_current_user(authorization)
            if not user:
                raise HTTPException(status_code=401, detail="Unauthorized")

            linked_username = self.database.get_linked_leetcode_username(user["id"])
            sync_data = self.database.get_leetcode_sync(linked_username) if linked_username else None
            payload = self._user_payload(user)
            payload["leetcodeUsername"] = linked_username

            return {"success": True, "data": {"user": payload, "leetcodeSync": sync_data}}

        @self.app.post("/api/auth/leetcode/link")
        async def link_leetcode(payload: LeetCodeLinkRequest, authorization: Optional[str] = Header(default=None)):
            """Link a LeetCode account to current user and optionally auto-sync"""
            user = self._get_current_user(authorization)
            if not user:
                raise HTTPException(status_code=401, detail="Unauthorized")

            profile = self.leetcode_api.get_user_profile(payload.username)
            if not profile:
                raise HTTPException(status_code=404, detail="LeetCode user not found")

            self.database.link_leetcode_account(user["id"], payload.username)
            sync_data = None
            if payload.auto_sync:
                sync_data = self._sync_leetcode_for_user(payload.username, user["id"])

            return {
                "success": True,
                "data": {
                    "linked": True,
                    "leetcodeUsername": payload.username,
                    "synced": payload.auto_sync,
                    "leetcodeSync": sync_data,
                },
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
        async def sync_leetcode(username: Optional[str] = None, authorization: Optional[str] = Header(default=None)):
            """Sync data from LeetCode account"""
            try:
                user = self._get_current_user(authorization)
                if user and not username:
                    username = self.database.get_linked_leetcode_username(user["id"])

                if not username:
                    raise HTTPException(status_code=400, detail="Provide username or link a LeetCode account first")

                logger.info(f"Starting LeetCode sync for: {username}")
                sync_data = self._sync_leetcode_for_user(username, user["id"] if user else None)

                return {"success": True, "data": sync_data, "message": "LeetCode sync completed"}
            except Exception as e:
                logger.error(f"Error syncing LeetCode: {e}")
                return {"success": False, "error": str(e)}
        
        @self.app.get("/api/leetcode/status")
        async def get_leetcode_status(authorization: Optional[str] = Header(default=None)):
            """Get LeetCode sync status"""
            try:
                user = self._get_current_user(authorization)
                linked_username = self.database.get_linked_leetcode_username(user["id"]) if user else None
                sync_data = self.database.get_leetcode_sync(linked_username) if linked_username else self.database.get_leetcode_sync()
                if sync_data:
                    return {
                        "success": True,
                        "data": sync_data,
                        "linked": bool(linked_username),
                        "leetcodeUsername": linked_username,
                    }
                else:
                    return {"success": True, "data": None, "message": "No LeetCode account linked"}
            except Exception as e:
                logger.error(f"Error fetching LeetCode status: {e}")
                return {"success": False, "error": str(e)}
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time communication"""
            await self.handle_websocket(websocket)

        @self.app.get("/{asset_path:path}")
        async def web_ui_assets(asset_path: str):
            """Serve web UI assets (renderer.js, CSS, etc.) with SPA fallback"""
            protected_prefixes = ("api/", "ws", "docs", "redoc", "openapi.json")
            if any(asset_path == prefix.rstrip("/") or asset_path.startswith(prefix) for prefix in protected_prefixes):
                raise HTTPException(status_code=404)

            asset_file = self.web_ui_dir / asset_path
            if asset_file.exists() and asset_file.is_file():
                return FileResponse(asset_file)

            index_file = self.web_ui_dir / "index.html"
            if index_file.exists():
                return FileResponse(index_file)

            raise HTTPException(status_code=404)
    
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
