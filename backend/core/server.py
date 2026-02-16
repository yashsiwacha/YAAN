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
