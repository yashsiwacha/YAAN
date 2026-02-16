"""
AI Engine - Local LLM Integration and Smart Response Generation
For conversational AI using transformers or fallback to rule-based responses
"""

from typing import Optional, List, Dict
import re

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from core.logger import setup_logger

logger = setup_logger("AIEngine")


class AIEngine:
    """Local LLM for conversational AI with smart fallback"""
    
    def __init__(self, config):
        self.config = config
        self.model = None
        self.tokenizer = None
        
        if TRANSFORMERS_AVAILABLE:
            self.device = "cuda" if torch.cuda.is_available() and config.use_gpu else "cpu"
        else:
            self.device = "cpu"
            logger.warning("Transformers library not available. Using rule-based responses.")
        
        self.context_memory: List[Dict[str, str]] = []
        self.knowledge_base = self._init_knowledge_base()
    
    def _init_knowledge_base(self) -> Dict[str, List[str]]:
        """Initialize knowledge base for fallback responses"""
        return {
            "greeting_responses": [
                "Hello! How can I assist you today?",
                "Hi there! What can I help you with?",
                "Greetings! Ready to help.",
            ],
            "coding_topics": [
                "I can help with programming questions! What language are you working with?",
                "Coding is my specialty! Are you working on a specific project?",
                "I'd be happy to help with code! What do you need?",
            ],
            "explanation_responses": [
                "That's an interesting topic! Let me explain...",
                "Good question! Here's what I know...",
                "I can help clarify that for you.",
            ],
        }
    
    def load_model(self):
        """Load language model (lazy loading)"""
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("Cannot load model: transformers library not installed")
            return
        
        if self.model is None:
            logger.info(f"Loading AI model: {self.config.model_name}")
            logger.info(f"Using device: {self.device}")
            
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.config.model_name,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
                )
                self.model.to(self.device)
                self.model.eval()
                
                logger.info("AI model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                raise
    
    def generate_response(self, prompt: str, max_length: Optional[int] = None) -> str:
        """
        Generate AI response to prompt
        
        Args:
            prompt: Input prompt
            max_length: Maximum response length
        
        Returns:
            Generated response text
        """
        # Use fallback if transformers not available or model not loaded
        if not TRANSFORMERS_AVAILABLE or self.model is None:
            return self._generate_fallback_response(prompt)
        
        max_length = max_length or self.config.max_tokens
        
        try:
            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=self.config.temperature,
                    do_sample=True,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the prompt from response
            if prompt in response:
                response = response.replace(prompt, "").strip()
            
            return response
            
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return self._generate_fallback_response(prompt)
    
    def _generate_fallback_response(self, prompt: str) -> str:
        """Generate smart fallback response when model is unavailable"""
        import random
        
        prompt_lower = prompt.lower()
        
        # Check for programming/tech keywords
        tech_keywords = ["code", "program", "function", "python", "javascript", "java", "c++", 
                        "algorithm", "debug", "error", "compile", "syntax"]
        if any(keyword in prompt_lower for keyword in tech_keywords):
            return random.choice(self.knowledge_base["coding_topics"])
        
        # Check for explanation requests
        explanation_keywords = ["explain", "what is", "how does", "why", "define", "meaning"]
        if any(keyword in prompt_lower for keyword in explanation_keywords):
            return random.choice(self.knowledge_base["explanation_responses"])
        
        # Check for greetings
        if any(greeting in prompt_lower for greeting in ["hello", "hi", "hey"]):
            return random.choice(self.knowledge_base["greeting_responses"])
        
        # Default responses
        default_responses = [
            "I understand you're asking about that. While I don't have detailed information without my full AI capabilities, I can still help with specific tasks!",
            "That's a good question! I'm currently running in lightweight mode. I can help with system tasks, calculations, and basic information.",
            "Interesting! For the best answers, consider asking me about time, system status, calculations, or type 'help' to see what I can do.",
        ]
        
        return random.choice(default_responses)
    
    def chat(self, messages: list) -> str:
        """
        Chat with context (conversation history)
        
        Args:
            messages: List of message dicts with 'role' and 'content'
        
        Returns:
            AI response
        """
        # Build conversation prompt
        prompt = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            prompt += f"{role.capitalize()}: {content}\n"
        prompt += "Assistant:"
        
        return self.generate_response(prompt)
