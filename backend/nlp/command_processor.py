"""
Command Processor - NLP and Intent Recognition
"""

import re
from datetime import datetime
from typing import Dict, Any, Optional
import platform
import psutil
from pathlib import Path

from core.logger import setup_logger
from user.profile import UserProfile
from user.memory import UserMemory
from nlp.coding_assistant import CodingAssistant
from nlp.reminder_system import ReminderSystem
from nlp.proactive_learning import ProactiveLearning

logger = setup_logger("CommandProcessor")


class CommandProcessor:
    """Process natural language commands and execute actions"""
    
    def __init__(self, config):
        self.config = config
        self.command_patterns = self._init_command_patterns()
        self.conversation_history = []
        self.context = {}
        self.last_intent = None
        
        # Initialize user memory system
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        self.profile = UserProfile(data_dir, config.user.name)
        self.memory = UserMemory(self.profile)
        
        # Initialize coding assistant
        self.coding_assistant = CodingAssistant()
        
        # Initialize reminder system
        self.reminder_system = ReminderSystem(data_dir / "reminders.db")
        
        # Initialize proactive learning
        self.proactive_learning = ProactiveLearning(data_dir / "learning.db")
        self.pending_question = None
        self.message_count = 0
        
        logger.info("Command processor initialized with user memory, coding assistant, reminder system, and proactive learning")
    
    def _init_command_patterns(self) -> Dict[str, list]:
        """Initialize command patterns for intent recognition"""
        return {
            "greeting": [
                r"^(hello|hi|hey|greetings|sup|yo)\b",
                r"good (morning|afternoon|evening|night)",
                r"how (are you|is it going)",
                r"what'?s up",
            ],
            "farewell": [
                r"(goodbye|bye|see you|farewell|later)",
                r"(exit|quit|close)",
                r"good night",
                r"catch you",
            ],
            "time": [
                r"what (is |'s )?the time",
                r"(tell me |what's |)the time",
                r"current time",
                r"time (now|right now)",
            ],
            "date": [
                r"what (is |'s )?the date",
                r"(tell me |what's |)today'?s date",
                r"what day is (it|today)",
                r"today'?s date",
            ],
            "weather": [
                r"(what'?s |how'?s |)the weather",
                r"weather (forecast|today|tomorrow|like)",
                r"(is it|will it) (rain|snow|sunny)",
            ],
            "system_info": [
                r"system (info|information|status|stats)",
                r"(cpu|memory|ram|disk) (usage|info|status)",
                r"how (is|'s) (my |the )?system",
                r"(check|show) (system|performance)",
            ],
            "open_app": [
                r"(open|launch|start|run) (.+)",
            ],
            "capabilities": [
                r"what (can|do) you (do|know)",
                r"(help|commands|capabilities|features)",
                r"how (can|do) you (help|assist)",
            ],
            "name_query": [
                r"(what'?s |who'?s |tell me )?your name",
                r"who are you",
                r"what are you",
            ],
            "thanks": [
                r"^(thanks|thank you|thx|ty)",
                r"(appreciate|grateful)",
            ],
            "affirmation": [
                r"^(yes|yeah|yep|sure|okay|ok|alright)",
                r"sounds good",
            ],
            "negation": [
                r"^(no|nope|nah|not really)",
            ],
            "joke": [
                r"(tell|make) (me )?(a )?joke",
                r"something funny",
                r"make me laugh",
            ],
            "reminder": [
                r"(set|create|add) (a )?reminder",
                r"remind me (to|about)",
            ],
            "calculation": [
                r"(calculate|compute) (.+)",
                r"\d+\s*[+\-*/]\s*\d+",
                r"what('?s| is) \d+",
            ],
            "memory_query": [
                r"what (do you know|have you learned) about me",
                r"what do you remember",
                r"tell me what you know about me",
                r"(my name|who am i)",
                r"what are my (interests|likes)",
            ],
            "forget_me": [
                r"forget (everything|all|me)",
                r"(clear|delete|erase) (my |your )?memory",
                r"(reset|remove) my (data|information)",
            ],
            "code_help": [
                r"(help|assist|explain) (with |me with )?(the |this |my )?code",
                r"(debug|fix|solve) (this |my )?code",
                r"what (does|is) this code",
                r"(explain|analyze|review) (this )?code",
                r"code (template|example|snippet)",
            ],
            "debug_error": [
                r"(debug|fix|solve) (this |my |the )?(error|bug|issue|problem)",
                r"(error|exception|crash|bug) (in|with|on)",
                r"(getting|got|received) (an |this )?error",
                r"(explain|help with|fix) (this |my |the )?error",
                r"why (is|does|am|getting)",
                r"(syntax|type|runtime|logic|null|undefined|reference) error",
            ],
            "code_explain": [
                r"explain (what is |the concept of )?(\w+)",
                r"what (is|are) (\w+)",
            ],
            "create_reminder": [
                r"remind me (to|about|at)",
                r"(set|create|add) (a )?reminder",
            ],
            "create_todo": [
                r"(add|create|make) (a |an )?todo",
                r"(add|create|make) (a |an )?task",
                r"^todo:[ ]",
                r"^task:[ ]",
            ],
            "show_reminders": [
                r"(show|list|get|display|view) (my |all )?reminders?",
                r"what are my reminders?",
                r"any reminders?",
            ],
            "show_todos": [
                r"(show|list|get|display|view) (my |all )?todos?",
                r"(show|list|get|display|view) (my |all )?tasks?",
                r"what are my (todos|tasks)?",
            ],
            "complete_task": [
                r"(complete|finish|done|mark) (reminder|todo|task) (\d+)",
                r"(reminder|todo|task) (\d+) (complete|done|finished)",
            ],
            "delete_task": [
                r"(delete|remove|clear) (reminder|todo|task) (\d+)",
            ],
            "task_summary": [
                r"(task|todo|reminder) summary",
                r"how many (tasks|todos|reminders)",
            ],
            "toggle_questions": [
                r"(stop|disable|turn off|enable|turn on) (asking )?(questions|learning)",
                r"(don't|do not) ask me questions",
                r"(start|begin) asking questions",
            ],
            "learning_summary": [
                r"learning (summary|progress|stats)",
                r"(show|what) (have )?(you )?learned",
                r"how much do you know",
            ],
        }
    
    def _match_intent(self, text: str) -> Optional[str]:
        """
        Match user input to intent
        
        Args:
            text: User input text
        
        Returns:
            Matched intent or None
        """
        text_lower = text.lower().strip()
        
        for intent, patterns in self.command_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent
        
        return None
    
    async def process(self, text: str) -> str:
        """
        Process user command and return response
        
        Args:
            text: User command text
        
        Returns:
            Response text
        """
        logger.info(f"Processing command: {text}")
        
        # Learn from user message
        self.memory.analyze_message(text)
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": text})
        
        # Keep only last 10 messages for context
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        # Check if memory can answer the query
        memory_response = self.memory.get_relevant_memory(text)
        if memory_response:
            logger.info("Responding from memory")
            self.conversation_history.append({"role": "assistant", "content": memory_response})
            self._save_interaction(text, memory_response)
            return memory_response
        
        # Match intent
        intent = self._match_intent(text)
        
        if intent:
            logger.info(f"Intent matched: {intent}")
            response = await self._execute_intent(intent, text)
            self.last_intent = intent
        else:
            # Fallback to general response
            response = await self._handle_general_query(text)
        
        # Add response to history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Save interaction and memory
        self._save_interaction(text, response)
        
        # Increment message count for proactive learning
        self.message_count += 1
        
        # Check if we should ask a proactive question
        if self.proactive_learning.should_ask_question(self.message_count):
            question_data = self.proactive_learning.get_next_question()
            if question_data:
                self.pending_question = question_data['question']
                # Append question to response
                response = f"{response}\n\n{question_data['formatted']}"
                logger.info(f"Added proactive question: {question_data['question']}")
        
        # Check if user's message is answering a pending question
        if self.pending_question:
            # Simple heuristic: if response is not a command, treat as answer
            if not intent or intent in ['greeting', 'thanks', 'affirmation']:
                self.proactive_learning.record_answer(self.pending_question, text)
                self.pending_question = None
                logger.info("Recorded answer to pending question")
        
        return response
    
    def _save_interaction(self, user_input: str, response: str):
        """Save interaction to profile and update memory"""
        self.profile.save_conversation(user_input, response)
        self.memory.save_memory()
    
    async def _execute_intent(self, intent: str, text: str) -> str:
        """Execute specific intent and return response"""
        
        intent_handlers = {
            "greeting": lambda: self._handle_greeting(),
            "farewell": lambda: self._handle_farewell(),
            "time": lambda: self._handle_time(),
            "date": lambda: self._handle_date(),
            "weather": lambda: self._handle_weather(),
            "system_info": lambda: self._handle_system_info(),
            "open_app": lambda: self._handle_open_app(text),
            "capabilities": lambda: self._handle_capabilities(),
            "name_query": lambda: self._handle_name_query(),
            "thanks": lambda: self._handle_thanks(),
            "affirmation": lambda: self._handle_affirmation(),
            "negation": lambda: self._handle_negation(),
            "joke": lambda: self._handle_joke(),
            "reminder": lambda: self._handle_reminder(text),
            "calculation": lambda: self._handle_calculation(text),
            "memory_query": lambda: self._handle_memory_query(text),
            "forget_me": lambda: self._handle_forget(),
            "code_help": lambda: self._handle_code_help(text),
            "code_explain": lambda: self._handle_code_explain(text),
            "debug_error": lambda: self._handle_debug_error(text),
            "create_reminder": lambda: self._handle_create_reminder(text),
            "create_todo": lambda: self._handle_create_todo(text),
            "show_reminders": lambda: self._handle_show_reminders(),
            "show_todos": lambda: self._handle_show_todos(),
            "complete_task": lambda: self._handle_complete_task(text),
            "delete_task": lambda: self._handle_delete_task(text),
            "task_summary": lambda: self._handle_task_summary(),
            "toggle_questions": lambda: self._handle_toggle_questions(text),
            "learning_summary": lambda: self._handle_learning_summary(),
        }
        
        handler = intent_handlers.get(intent)
        if handler:
            return handler()
        
        return "I'm not sure how to help with that yet."
    
    def _handle_greeting(self) -> str:
        """Handle greeting with personalization"""
        import random
        
        # Use memory to get personalized greeting
        if self.memory.user_facts.get("name"):
            return self.memory.get_personalized_greeting()
        
        hour = datetime.now().hour
        if hour < 12:
            time_greeting = "Good morning"
        elif hour < 18:
            time_greeting = "Good afternoon"
        else:
            time_greeting = "Good evening"
        
        # Check conversation history for repeated greetings
        recent_greetings = sum(1 for msg in self.conversation_history[-6:] 
                              if msg.get("role") == "user" and "hello" in msg.get("content", "").lower())
        
        if recent_greetings > 1:
            responses = [
                "Hello again! What else can I help you with?",
                "Still here! What do you need?",
                "Yes, how can I assist you?",
            ]
            return random.choice(responses)
        
        responses = [
            f"{time_greeting}! How can I help you today?",
            f"{time_greeting}! What can I do for you?",
            f"Hello! Ready to assist you.",
            f"Hi there! How may I help?",
        ]
        
        return random.choice(responses)
    
    def _handle_farewell(self) -> str:
        """Handle farewell"""
        return f"Goodbye, {self.config.user.name}! Have a great day!"
    
    def _handle_time(self) -> str:
        """Handle time query"""
        now = datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}"
    
    def _handle_date(self) -> str:
        """Handle date query"""
        now = datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}"
    
    def _handle_weather(self) -> str:
        """Handle weather query (offline - limited)"""
        return "I can't check the weather while offline. Please connect to the internet for weather updates."
    
    def _handle_system_info(self) -> str:
        """Handle system information query"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info = f"""System Status:
- OS: {platform.system()} {platform.release()}
- CPU Usage: {cpu_percent}%
- Memory: {memory.percent}% used ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)
- Disk: {disk.percent}% used ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)"""
            
            return info
        except Exception as e:
            logger.error(f"System info error: {e}")
            return "Unable to retrieve system information."
    
    def _handle_open_app(self, text: str) -> str:
        """Handle opening applications"""
        # Extract app name
        match = re.search(r"(open|launch|start|run) (.+)", text.lower())
        if match:
            app_name = match.group(2).strip()
            return f"I'll try to open {app_name} for you. (Feature coming soon)"
        return "Which application would you like to open?"
    
    def _handle_capabilities(self) -> str:
        """Handle capabilities/help request"""
        help_text = """I can assist you with:

🕐 Time & Date - "What time is it?" or "What's today's date?"
💻 System Info - "How's my system?" or "Check CPU usage"
🗣️ Conversation - I can chat about various topics
🧮 Math - "Calculate 25 * 4" or simple arithmetic
😄 Entertainment - "Tell me a joke"

💻 Code Help (15+ Languages!) - "Explain this code: def hello()..." 
🐛 Debug Errors - "Debug this error: TypeError..." or "Fix my code"
   Supports: Python, JavaScript, TypeScript, Java, C++, C, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, SQL, HTML, CSS
📚 Programming Concepts - "What is recursion?" or "Explain polymorphism"
🎯 Code Templates - Request templates for functions, classes, or patterns
🔍 Error Analysis - Share error messages and I'll explain the cause and solution

⏰ Reminders - "Remind me to call John tomorrow at 3pm"
✅ Todos - "Add todo: finish project #work" or "Create task: review code [high]"
📋 Task Management - "Show my reminders", "Complete todo 1", "Task summary"

🧠 Memory - I learn about you! Ask "What do you know about me?"
🎓 Proactive Learning - I'll ask questions to understand you better (max 2/day)
🌤️ Weather - Coming soon when online
🚀 Open Apps - Launch applications (in development)

I learn about your preferences, coding style, and communication patterns as we talk!
Just speak naturally, and I'll do my best to understand and help!"""
        return help_text
    
    def _handle_name_query(self) -> str:
        """Handle name/identity query"""
        return "I'm YAAN - Your AI Assistant Network. I'm here to help you with various tasks and answer your questions."
    
    def _handle_thanks(self) -> str:
        """Handle gratitude"""
        import random
        responses = [
            "You're welcome!",
            "Happy to help!",
            "Anytime!",
            "My pleasure!",
            "Glad I could assist!",
        ]
        return random.choice(responses)
    
    def _handle_affirmation(self) -> str:
        """Handle yes/affirmation"""
        if self.last_intent:
            return "Great! What would you like to do next?"
        return "Alright! How can I help you?"
    
    def _handle_negation(self) -> str:
        """Handle no/negation"""
        return "No problem. Is there anything else I can help you with?"
    
    def _handle_joke(self) -> str:
        """Handle joke request"""
        import random
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            "Why did the developer go broke? Because he used up all his cache! 💰",
            "What's a computer's favorite snack? Microchips! 🍪",
            "Why don't robots ever panic? Because they have nerves of steel! 🤖",
            "How do you comfort a JavaScript bug? You console it! 😄",
        ]
        return random.choice(jokes)
    
    def _handle_reminder(self, text: str) -> str:
        """Handle reminder creation"""
        # Extract what to remind about
        match = re.search(r"remind me (to|about) (.+)", text.lower())
        if match:
            reminder_text = match.group(2).strip()
            self.context['pending_reminder'] = reminder_text
            return f"I'll note that down: '{reminder_text}'. Reminder functionality is coming soon!"
        return "What would you like me to remind you about?"
    
    def _handle_calculation(self, text: str) -> str:
        """Handle simple mathematical calculations"""
        try:
            # Extract mathematical expression
            match = re.search(r"(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)", text)
            if match:
                num1 = float(match.group(1))
                operator = match.group(2)
                num2 = float(match.group(3))
                
                operations = {
                    '+': lambda a, b: a + b,
                    '-': lambda a, b: a - b,
                    '*': lambda a, b: a * b,
                    '/': lambda a, b: a / b if b != 0 else None,
                }
                
                result = operations[operator](num1, num2)
                if result is not None:
                    # Format result nicely
                    if result == int(result):
                        return f"{num1} {operator} {num2} = {int(result)}"
                    else:
                        return f"{num1} {operator} {num2} = {result:.2f}"
                else:
                    return "Cannot divide by zero!"
            
            return "I can help with simple calculations like '25 + 17' or '100 / 4'. Try asking me!"
        except Exception as e:
            logger.error(f"Calculation error: {e}")
            return "Sorry, I couldn't calculate that. Try a simpler expression like '10 + 5'."
    
    def _handle_memory_query(self, text: str) -> str:
        """Handle queries about what the AI remembers"""
        return self.memory.get_memory_summary()
    
    def _handle_forget(self) -> str:
        """Handle request to forget user data"""
        self.memory.forget_user_data()
        return "I've cleared all my memories about you. We can start fresh! Feel free to tell me about yourself again."
    
    async def _handle_general_query(self, text: str) -> str:
        """Handle general queries (fallback with smarter responses)"""
        import random
        
        text_lower = text.lower()
        
        # Context-aware responses
        if any(word in text_lower for word in ["love", "like", "favorite"]):
            return "I appreciate the sentiment! I'm here to help you with tasks and information. What can I do for you?"
        
        if any(word in text_lower for word in ["how are you", "how do you feel"]):
            return "I'm functioning perfectly, thank you for asking! How can I assist you today?"
        
        if "create" in text_lower or "make" in text_lower:
            return "I can help with various tasks! Try asking me about time, date, system info, calculations, or just chat. What would you like to do?"
        
        if "learn" in text_lower or "teach" in text_lower:
            return "I'm continuously learning and improving! Right now I can help with time, dates, system monitoring, math, and conversation. Type 'help' to see all my capabilities."
        
        if any(word in text_lower for word in ["where", "location", "place"]):
            return "I don't have access to location services yet. I can help with other things though - try asking about time, system info, or calculations!"
        
        if "why" in text_lower:
            responses = [
                "That's a great question! While I don't have that specific information, I can help you with time, dates, system info, and more. What would you like to know?",
                "Interesting question! I'm still learning about complex topics. Try asking me something about your system or request calculations.",
            ]
            return random.choice(responses)
        
        if any(word in text_lower for word in ["code", "program", "script"]):
            return "I can help with technical questions! I know about system information, can do calculations, and provide helpful information. What do you need?"
        
        # Check if it's a question
        if "?" in text or text_lower.startswith(("what", "when", "where", "who", "how", "why", "can", "could", "would", "should")):
            responses = [
                "I don't have that specific information yet, but I'm always learning! Try asking me about time, date, system status, or calculations.",
                "Great question! While I don't know the answer to that, I can help you with system information, calculations, and more. Type 'help' to see what I can do.",
                "Hmm, I'm not sure about that one. I'm best at helping with system tasks, calculations, and providing information about time and dates. What can I help you with?",
            ]
            return random.choice(responses)
        
        # General fallback
        responses = [
            "I'm not quite sure what you mean. Could you rephrase that, or try asking me about time, system info, or calculations?",
            "Interesting! I'm still learning about that topic. I can help you with time, dates, system monitoring, and math though. What would you like?",
            "I don't fully understand that yet. Type 'help' to see what I can assist you with!",
            "Could you rephrase that? I'm best at helping with specific tasks like checking the time, system stats, or doing calculations.",
        ]
        
        return random.choice(responses)
    def _handle_code_help(self, text: str) -> str:
        """Handle code-related help requests"""
        try:
            # Check if text contains code
            code_indicators = ['def ', 'class ', 'function ', 'for ', 'while ', 'if ', 'import ', 'include ', 'void ', 'int ', 'public ', 'private']
            has_code = any(indicator in text.lower() for indicator in code_indicators)
            
            if has_code:
                # Provide explanation
                explanation = self.coding_assistant.explain_code(text)
                
                # Check for common errors and provide debugging help
                if any(word in text.lower() for word in ['error', 'bug', 'issue', 'problem', 'wrong', 'crash']):
                    debug_info = self.coding_assistant.debug_help(text)
                    return f"{explanation}\n\n{debug_info}"
                
                return explanation
            else:
                return "Please share the code you need help with, and I'll explain it or help debug any issues!"
                
        except Exception as e:
            logger.error(f"Error in code help: {e}")
            return "I encountered an issue analyzing the code. Please try again or rephrase your request."
    
    def _handle_code_explain(self, text: str) -> str:
        """Handle programming concept explanation requests"""
        try:
            # Extract the concept from text
            concept = text.lower()
            for phrase in ['what is', 'explain', 'tell me about', 'what are']:
                if phrase in concept:
                    concept = concept.split(phrase)[-1].strip()
                    break
            
            # Remove trailing question marks
            concept = concept.rstrip('?').strip()
            
            if concept:
                explanation = self.coding_assistant.generate_explanation(concept)
                if explanation:
                    return explanation
                else:
                    # Concept not in database, provide general response
                    return f"I don't have a detailed explanation for '{concept}' yet, but I can help with:\n\n• Variables, functions, loops, arrays\n• Classes, objects, recursion\n• Algorithms, APIs, async programming\n• Specific programming languages\n• Code debugging and optimization\n\nTry asking about these topics, or share some code for me to explain!"
            else:
                return "What programming concept would you like me to explain? For example, try asking 'explain loops' or 'what is recursion?'"
                
        except Exception as e:
            logger.error(f"Error explaining concept: {e}")
            return "I encountered an issue explaining that concept. Please try again."
    
    def _handle_debug_error(self, text: str) -> str:
        """Handle debugging and error explanation requests"""
        try:
            # Extract error message and code from text
            error_msg = text
            code_snippet = None
            
            # Try to extract code blocks (markdown style)
            code_match = re.search(r'```[\w]*\n(.*?)```', text, re.DOTALL)
            if code_match:
                code_snippet = code_match.group(1).strip()
                error_msg = text.replace(code_match.group(0), '').strip()
            
            # If no markdown, look for lines with typical code patterns
            elif ':' in text or '{' in text or 'def ' in text or 'function ' in text:
                lines = text.split('\n')
                code_lines = []
                error_lines = []
                
                for line in lines:
                    # Heuristic: lines with typical code characters are code
                    if any(char in line for char in ['(', ')', '{', '}', ';', ':', '=']) and not line.lower().startswith(('error', 'exception', 'traceback')):
                        code_lines.append(line)
                    else:
                        error_lines.append(line)
                
                if code_lines:
                    code_snippet = '\n'.join(code_lines)
                if error_lines:
                    error_msg = '\n'.join(error_lines).strip()
            
            # Get debugging help from coding assistant
            if code_snippet or any(word in text.lower() for word in ['error', 'exception', 'bug', 'crash', 'issue', 'problem', 'fail']):
                debug_response = self.coding_assistant.debug_help(error_msg, code_snippet)
                return debug_response
            else:
                return """I can help debug your code! Please share:

1. **The error message** you're getting (copy-paste it)
2. **The code** that's causing the error
3. **What you expected** to happen

**Example:**
```
I'm getting this error:
TypeError: unsupported operand type(s) for +: 'int' and 'str'

Code:
x = 5
y = "10"
result = x + y
```

I'll analyze it and help you fix it!"""
                
        except Exception as e:
            logger.error(f"Error in debug help: {e}")
            return "I encountered an issue analyzing the error. Please share the error message and code, and I'll help you debug it."
    
    def _handle_create_reminder(self, text: str) -> str:
        """Handle reminder creation from natural language"""
        try:
            reminder_data = self.reminder_system.parse_reminder_from_text(text)
            
            if reminder_data:
                reminder_id = self.reminder_system.create_reminder(
                    title=reminder_data['title'],
                    description=reminder_data.get('description', ''),
                    due_date=reminder_data.get('due_date'),
                    due_time=reminder_data.get('due_time'),
                    priority=reminder_data.get('priority', 'medium')
                )
                
                if reminder_id:
                    due_info = ""
                    if reminder_data.get('due_date'):
                        due_info = f" for {reminder_data['due_date']}"
                        if reminder_data.get('due_time'):
                            due_info += f" at {reminder_data['due_time']}"
                    
                    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(reminder_data.get('priority', 'medium'), "🟡")
                    
                    return f"✅ Reminder created{due_info}!\n{priority_emoji} {reminder_data['title']}"
                else:
                    return "Sorry, I couldn't create the reminder. Please try again."
            else:
                return "I couldn't understand the reminder. Try something like 'remind me to call John tomorrow at 3pm'"
                
        except Exception as e:
            logger.error(f"Error creating reminder: {e}")
            return "I encountered an issue creating the reminder. Please try again."
    
    def _handle_create_todo(self, text: str) -> str:
        """Handle todo creation from natural language"""
        try:
            todo_data = self.reminder_system.parse_todo_from_text(text)
            
            if todo_data:
                todo_id = self.reminder_system.create_todo(
                    title=todo_data['title'],
                    description=todo_data.get('description', ''),
                    priority=todo_data.get('priority', 'medium'),
                    category=todo_data.get('category', 'general'),
                    tags=todo_data.get('tags', [])
                )
                
                if todo_id:
                    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(todo_data.get('priority', 'medium'), "🟡")
                    tags_str = " " + " ".join(f"#{tag}" for tag in todo_data.get('tags', [])) if todo_data.get('tags') else ""
                    
                    return f"✅ Todo added!\n{priority_emoji} {todo_data['title']}{tags_str}"
                else:
                    return "Sorry, I couldn't create the todo. Please try again."
            else:
                return "I couldn't understand the todo. Try something like 'add todo: finish project #work' or 'create task: buy groceries [high]'"
                
        except Exception as e:
            logger.error(f"Error creating todo: {e}")
            return "I encountered an issue creating the todo. Please try again."
    
    def _handle_show_reminders(self) -> str:
        """Handle displaying reminders"""
        try:
            reminders = self.reminder_system.get_reminders(status='pending')
            
            if reminders:
                formatted = self.reminder_system.format_reminders_list(reminders)
                return f"📋 Your Reminders:\n\n{formatted}"
            else:
                return "You have no pending reminders. Add one with 'remind me to [task]'!"
                
        except Exception as e:
            logger.error(f"Error showing reminders: {e}")
            return "I encountered an issue retrieving your reminders. Please try again."
    
    def _handle_show_todos(self) -> str:
        """Handle displaying todos"""
        try:
            todos = self.reminder_system.get_todos(status='pending')
            
            if todos:
                formatted = self.reminder_system.format_todos_list(todos)
                return f"✅ Your Todos:\n\n{formatted}"
            else:
                return "You have no pending todos. Add one with 'add todo: [task]'!"
                
        except Exception as e:
            logger.error(f"Error showing todos: {e}")
            return "I encountered an issue retrieving your todos. Please try again."
    
    def _handle_complete_task(self, text: str) -> str:
        """Handle marking tasks as complete"""
        try:
            import re
            
            # Extract task type (reminder or todo) and ID
            is_reminder = 'reminder' in text.lower()
            is_todo = 'todo' in text.lower() or 'task' in text.lower()
            
            # Extract numeric ID
            numbers = re.findall(r'\d+', text)
            
            if not numbers:
                return "Please specify which task to complete. Example: 'complete reminder 1' or 'complete todo 3'"
            
            task_id = int(numbers[0])
            
            if is_reminder:
                success = self.reminder_system.complete_reminder(task_id)
                if success:
                    return f"✅ Reminder #{task_id} marked as complete!"
                else:
                    return f"Couldn't find reminder #{task_id}. Check your list with 'show reminders'."
            elif is_todo:
                success = self.reminder_system.complete_todo(task_id)
                if success:
                    return f"✅ Todo #{task_id} marked as complete!"
                else:
                    return f"Couldn't find todo #{task_id}. Check your list with 'show todos'."
            else:
                return "Please specify 'reminder' or 'todo'. Example: 'complete reminder 1' or 'complete todo 3'"
                
        except Exception as e:
            logger.error(f"Error completing task: {e}")
            return "I encountered an issue completing the task. Please try again."
    
    def _handle_delete_task(self, text: str) -> str:
        """Handle deleting tasks"""
        try:
            import re
            
            # Extract task type (reminder or todo) and ID
            is_reminder = 'reminder' in text.lower()
            is_todo = 'todo' in text.lower() or 'task' in text.lower()
            
            # Extract numeric ID
            numbers = re.findall(r'\d+', text)
            
            if not numbers:
                return "Please specify which task to delete. Example: 'delete reminder 1' or 'delete todo 3'"
            
            task_id = int(numbers[0])
            
            if is_reminder:
                success = self.reminder_system.delete_reminder(task_id)
                if success:
                    return f"🗑️ Reminder #{task_id} deleted."
                else:
                    return f"Couldn't find reminder #{task_id}. Check your list with 'show reminders'."
            elif is_todo:
                success = self.reminder_system.delete_todo(task_id)
                if success:
                    return f"🗑️ Todo #{task_id} deleted."
                else:
                    return f"Couldn't find todo #{task_id}. Check your list with 'show todos'."
            else:
                return "Please specify 'reminder' or 'todo'. Example: 'delete reminder 1' or 'delete todo 3'"
                
        except Exception as e:
            logger.error(f"Error deleting task: {e}")
            return "I encountered an issue deleting the task. Please try again."
    
    def _handle_task_summary(self) -> str:
        """Handle showing task summary"""
        try:
            summary = self.reminder_system.get_summary()
            return summary
                
        except Exception as e:
            logger.error(f"Error getting task summary: {e}")
            return "I encountered an issue retrieving your task summary. Please try again."
    
    def _handle_toggle_questions(self, text: str) -> str:
        """Handle toggling proactive learning questions on/off"""
        try:
            # Determine if user wants to enable or disable
            text_lower = text.lower()
            if any(word in text_lower for word in ["stop", "disable", "turn off", "off"]):
                self.proactive_learning.toggle_questions(False)
                return "✅ I've disabled proactive learning questions. I won't ask you questions to learn anymore. You can re-enable them anytime by saying 'enable learning questions'."
            elif any(word in text_lower for word in ["enable", "turn on", "start", "on"]):
                self.proactive_learning.toggle_questions(True)
                return "✅ I've enabled proactive learning questions. I'll occasionally ask you questions to learn more about your preferences and help you better. You can disable them anytime by saying 'stop asking questions'."
            else:
                # Toggle current state
                current_state = self.proactive_learning.toggle_questions(None)  # Get current state
                if current_state:
                    self.proactive_learning.toggle_questions(False)
                    return "✅ Proactive learning questions are now OFF."
                else:
                    self.proactive_learning.toggle_questions(True)
                    return "✅ Proactive learning questions are now ON."
                    
        except Exception as e:
            logger.error(f"Error toggling questions: {e}")
            return "I encountered an issue toggling the learning questions. Please try again."
    
    def _handle_learning_summary(self) -> str:
        """Handle showing learning summary"""
        try:
            summary = self.proactive_learning.get_learning_summary()
            recent = self.proactive_learning.get_recent_questions(5)
            
            response = "📊 **Learning Summary**\n\n"
            response += f"**Questions Asked:** {summary['total_asked']}\n"
            response += f"**Questions Answered:** {summary['answered']}\n"
            response += f"**Today's Questions:** {summary['asked_today']}/{summary['max_per_day']}\n\n"
            
            if summary['by_category']:
                response += "**By Category:**\n"
                for category, count in summary['by_category'].items():
                    response += f"- {category.title()}: {count} questions\n"
            
            if recent:
                response += "\n**Recent Questions:**\n"
                for i, q in enumerate(recent, 1):
                    status = "✅ Answered" if q['answered'] else "⏸️ Pending"
                    response += f"{i}. [{q['category']}] {q['question']} - {status}\n"
            
            return response
                
        except Exception as e:
            logger.error(f"Error getting learning summary: {e}")
            return "I encountered an issue retrieving the learning summary. Please try again."