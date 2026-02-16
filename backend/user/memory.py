"""
User Memory and Learning System
Learns about user preferences, communication style, and personal information
"""

import re
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import Counter

from user.profile import UserProfile
from core.logger import setup_logger

logger = setup_logger("UserMemory")


class UserMemory:
    """Advanced memory system that learns about the user"""
    
    def __init__(self, profile: UserProfile):
        self.profile = profile
        self.session_data = {
            "topics_discussed": [],
            "communication_style": {},
            "interaction_count": 0,
            "session_start": datetime.now()
        }
        
        # Load persistent memory
        self._load_persistent_memory()
    
    def _load_persistent_memory(self):
        """Load learned information from database"""
        self.user_facts = self.profile.get_preference("user_facts", {})
        self.interests = self.profile.get_preference("interests", {})
        self.communication_style = self.profile.get_preference("communication_style", {
            "formality": "neutral",  # casual, neutral, formal
            "verbosity": "medium",   # brief, medium, detailed
            "emoji_usage": False,
            "avg_message_length": 0,
            "common_phrases": [],
            "preferred_greeting": "Hello"
        })
        
        logger.info("User memory loaded")
    
    def analyze_message(self, message: str):
        """Analyze user message to learn communication patterns"""
        self.session_data["interaction_count"] += 1
        
        # Analyze message length
        msg_length = len(message.split())
        self._update_avg_message_length(msg_length)
        
        # Detect communication style
        self._detect_formality(message)
        self._detect_emoji_usage(message)
        self._extract_common_phrases(message)
        
        # Extract topics
        topics = self._extract_topics(message)
        self.session_data["topics_discussed"].extend(topics)
        
        # Learn about user interests
        self._update_interests(topics)
        
        # Extract potential personal facts
        self._extract_user_facts(message)
    
    def _update_avg_message_length(self, new_length: int):
        """Update running average of message length"""
        current_avg = self.communication_style.get("avg_message_length", 0)
        total_messages = self.profile.get_preference("total_messages", 0) + 1
        
        new_avg = ((current_avg * (total_messages - 1)) + new_length) / total_messages
        self.communication_style["avg_message_length"] = round(new_avg, 2)
        
        # Update verbosity based on average length
        if new_avg < 5:
            self.communication_style["verbosity"] = "brief"
        elif new_avg > 15:
            self.communication_style["verbosity"] = "detailed"
        else:
            self.communication_style["verbosity"] = "medium"
        
        self.profile.set_preference("total_messages", total_messages)
    
    def _detect_formality(self, message: str):
        """Detect if user prefers formal or casual communication"""
        casual_indicators = [
            r"\b(hey|hi|sup|yo|yeah|yep|nah|gonna|wanna|gotta)\b",
            r"[!]{2,}",  # Multiple exclamation marks
            r"\blol\b|\blmao\b|\bhaha\b"
        ]
        
        formal_indicators = [
            r"\b(greetings|please|thank you|could you|would you|sir|madam)\b",
            r"\b(kindly|appreciate|grateful)\b"
        ]
        
        casual_score = sum(1 for pattern in casual_indicators if re.search(pattern, message.lower()))
        formal_score = sum(1 for pattern in formal_indicators if re.search(pattern, message.lower()))
        
        if casual_score > formal_score:
            self.communication_style["formality"] = "casual"
        elif formal_score > casual_score:
            self.communication_style["formality"] = "formal"
        else:
            self.communication_style["formality"] = "neutral"
    
    def _detect_emoji_usage(self, message: str):
        """Detect if user uses emojis"""
        emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]'
        has_emoji = bool(re.search(emoji_pattern, message))
        
        if has_emoji:
            self.communication_style["emoji_usage"] = True
    
    def _extract_common_phrases(self, message: str):
        """Track commonly used phrases"""
        # Extract 2-3 word phrases
        words = message.lower().split()
        if len(words) >= 2:
            bigrams = [' '.join(words[i:i+2]) for i in range(len(words)-1)]
            
            common_phrases = self.communication_style.get("common_phrases", [])
            common_phrases.extend(bigrams)
            
            # Keep only most common phrases (top 20)
            if len(common_phrases) > 50:
                phrase_counts = Counter(common_phrases)
                self.communication_style["common_phrases"] = [
                    phrase for phrase, _ in phrase_counts.most_common(20)
                ]
            else:
                self.communication_style["common_phrases"] = common_phrases
    
    def _extract_topics(self, message: str) -> List[str]:
        """Extract topics from message"""
        topics = []
        
        topic_keywords = {
            "programming": ["code", "program", "script", "python", "java", "javascript", "function", "debug"],
            "work": ["work", "job", "office", "project", "meeting", "deadline", "boss"],
            "technology": ["computer", "system", "software", "hardware", "tech", "ai", "ml"],
            "personal": ["i am", "i like", "i love", "i want", "my", "me"],
            "entertainment": ["movie", "game", "music", "video", "watch", "play"],
            "learning": ["learn", "study", "teach", "tutorial", "course", "understand"],
            "health": ["exercise", "health", "fitness", "sleep", "diet"],
            "hobbies": ["hobby", "interest", "enjoy", "fun", "leisure"],
        }
        
        message_lower = message.lower()
        for topic, keywords in topic_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _update_interests(self, topics: List[str]):
        """Update user interests based on discussed topics"""
        for topic in topics:
            self.interests[topic] = self.interests.get(topic, 0) + 1
        
        # Keep track of top interests
        if len(self.interests) > 0:
            sorted_interests = sorted(self.interests.items(), key=lambda x: x[1], reverse=True)
            logger.info(f"Top user interests: {sorted_interests[:3]}")
    
    def _extract_user_facts(self, message: str):
        """Extract personal facts about the user"""
        message_lower = message.lower()
        
        # Extract name
        name_match = re.search(r"(my name is|i'm|i am|call me) (\w+)", message_lower)
        if name_match:
            name = name_match.group(2).capitalize()
            self.user_facts["name"] = name
            self.profile.user_name = name
            logger.info(f"Learned user name: {name}")
        
        # Extract location
        location_match = re.search(r"(i live in|i'm from|located in) ([\w\s]+)", message_lower)
        if location_match:
            location = location_match.group(2).strip()
            self.user_facts["location"] = location
            logger.info(f"Learned user location: {location}")
        
        # Extract occupation
        occupation_match = re.search(r"(i work as|i am a|i'm a) ([\w\s]+)", message_lower)
        if occupation_match:
            occupation = occupation_match.group(2).strip()
            self.user_facts["occupation"] = occupation
            logger.info(f"Learned user occupation: {occupation}")
        
        # Extract likes/preferences
        likes_match = re.search(r"i (like|love|enjoy|prefer) ([\w\s]+)", message_lower)
        if likes_match:
            liked_thing = likes_match.group(2).strip()
            likes = self.user_facts.get("likes", [])
            if liked_thing not in likes:
                likes.append(liked_thing)
                self.user_facts["likes"] = likes
                logger.info(f"Learned user likes: {liked_thing}")
        
        # Extract dislikes
        dislikes_match = re.search(r"i (don't like|hate|dislike) ([\w\s]+)", message_lower)
        if dislikes_match:
            disliked_thing = dislikes_match.group(2).strip()
            dislikes = self.user_facts.get("dislikes", [])
            if disliked_thing not in dislikes:
                dislikes.append(disliked_thing)
                self.user_facts["dislikes"] = dislikes
                logger.info(f"Learned user dislikes: {disliked_thing}")
    
    def get_personalized_greeting(self) -> str:
        """Get personalized greeting based on learned preferences"""
        formality = self.communication_style.get("formality", "neutral")
        user_name = self.user_facts.get("name", "there")
        
        if formality == "casual":
            greetings = [f"Hey {user_name}!", f"Hi {user_name}!", f"What's up {user_name}?"]
        elif formality == "formal":
            greetings = [f"Good day, {user_name}.", f"Greetings, {user_name}.", f"Hello, {user_name}."]
        else:
            greetings = [f"Hello {user_name}!", f"Hi {user_name}!", f"Hey there {user_name}!"]
        
        import random
        return random.choice(greetings)
    
    def get_context_for_response(self) -> Dict[str, Any]:
        """Get contextual information to personalize responses"""
        return {
            "user_name": self.user_facts.get("name", ""),
            "formality": self.communication_style.get("formality", "neutral"),
            "verbosity": self.communication_style.get("verbosity", "medium"),
            "top_interests": sorted(self.interests.items(), key=lambda x: x[1], reverse=True)[:3],
            "known_facts": self.user_facts,
            "session_topics": list(set(self.session_data["topics_discussed"]))
        }
    
    def get_relevant_memory(self, query: str) -> Optional[str]:
        """Retrieve relevant information from memory based on query"""
        query_lower = query.lower()
        
        # Check if query relates to stored facts
        if "my name" in query_lower or "who am i" in query_lower:
            name = self.user_facts.get("name")
            if name:
                return f"Your name is {name}."
        
        if "where" in query_lower and ("live" in query_lower or "from" in query_lower):
            location = self.user_facts.get("location")
            if location:
                return f"You mentioned you're from {location}."
        
        if "what do i" in query_lower and "like" in query_lower:
            likes = self.user_facts.get("likes", [])
            if likes:
                return f"You've mentioned you like: {', '.join(likes)}."
        
        # Check recent topics
        recent_topics = self.session_data["topics_discussed"][-5:]
        if recent_topics:
            topics_str = ", ".join(set(recent_topics))
            if "what were we talking about" in query_lower or "what did we discuss" in query_lower:
                return f"We've been discussing: {topics_str}."
        
        return None
    
    def save_memory(self):
        """Persist learned information to database"""
        self.profile.set_preference("user_facts", self.user_facts)
        self.profile.set_preference("interests", self.interests)
        self.profile.set_preference("communication_style", self.communication_style)
        
        # Log learning summary
        logger.info(f"Memory saved - Known facts: {len(self.user_facts)}, Interests: {len(self.interests)}")
    
    def get_memory_summary(self) -> str:
        """Get a summary of what the AI has learned about the user"""
        summary_parts = []
        
        # Name
        if "name" in self.user_facts:
            summary_parts.append(f"• Your name: {self.user_facts['name']}")
        
        # Location
        if "location" in self.user_facts:
            summary_parts.append(f"• Location: {self.user_facts['location']}")
        
        # Occupation
        if "occupation" in self.user_facts:
            summary_parts.append(f"• Occupation: {self.user_facts['occupation']}")
        
        # Interests
        if self.interests:
            top_interests = sorted(self.interests.items(), key=lambda x: x[1], reverse=True)[:3]
            interests_str = ", ".join([interest for interest, _ in top_interests])
            summary_parts.append(f"• Main interests: {interests_str}")
        
        # Communication style
        formality = self.communication_style.get("formality", "neutral")
        summary_parts.append(f"• Communication style: {formality}")
        
        # Likes
        if "likes" in self.user_facts and self.user_facts["likes"]:
            likes_str = ", ".join(self.user_facts["likes"][:3])
            summary_parts.append(f"• You like: {likes_str}")
        
        if summary_parts:
            return "Here's what I've learned about you:\n\n" + "\n".join(summary_parts)
        else:
            return "I'm still learning about you! Keep chatting with me so I can understand your preferences better."
    
    def forget_user_data(self):
        """Clear all learned user data (privacy feature)"""
        self.user_facts = {}
        self.interests = {}
        self.communication_style = {
            "formality": "neutral",
            "verbosity": "medium",
            "emoji_usage": False,
            "avg_message_length": 0,
            "common_phrases": [],
            "preferred_greeting": "Hello"
        }
        self.save_memory()
        logger.info("User memory cleared")
