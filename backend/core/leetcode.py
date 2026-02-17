"""
LeetCode Integration Module
Fetches user statistics and solved problems from LeetCode
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

from core.logger import setup_logger

logger = setup_logger("LeetCode")


class LeetCodeAPI:
    """LeetCode GraphQL API client"""
    
    def __init__(self):
        self.base_url = "https://leetcode.com/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "YAAN-Desktop/1.0"
        }
    
    def get_user_profile(self, username: str) -> Optional[Dict[str, Any]]:
        """Fetch user profile data"""
        query = """
        query getUserProfile($username: String!) {
            matchedUser(username: $username) {
                username
                profile {
                    realName
                    userAvatar
                    ranking
                }
                submitStats {
                    acSubmissionNum {
                        difficulty
                        count
                        submissions
                    }
                }
            }
        }
        """
        
        try:
            response = requests.post(
                self.base_url,
                json={
                    "query": query,
                    "variables": {"username": username}
                },
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("data", {}).get("matchedUser"):
                    return data["data"]["matchedUser"]
                else:
                    logger.error(f"User not found: {username}")
                    return None
            else:
                logger.error(f"API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching profile: {e}")
            return None
    
    def get_user_stats(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user's solved problem statistics"""
        query = """
        query userProblemsSolved($username: String!) {
            allQuestionsCount {
                difficulty
                count
            }
            matchedUser(username: $username) {
                submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                        submissions
                    }
                }
                userCalendar {
                    activeYears
                    streak
                    totalActiveDays
                    submissionCalendar
                }
            }
        }
        """
        
        try:
            response = requests.post(
                self.base_url,
                json={
                    "query": query,
                    "variables": {"username": username}
                },
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("data", {})
            else:
                logger.error(f"API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching stats: {e}")
            return None
    
    def get_recent_submissions(self, username: str, limit: int = 20) -> Optional[List[Dict[str, Any]]]:
        """Get user's recent submissions"""
        query = """
        query recentAcSubmissions($username: String!, $limit: Int!) {
            recentAcSubmissionList(username: $username, limit: $limit) {
                id
                title
                titleSlug
                timestamp
            }
        }
        """
        
        try:
            response = requests.post(
                self.base_url,
                json={
                    "query": query,
                    "variables": {"username": username, "limit": limit}
                },
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("data", {}).get("recentAcSubmissionList", [])
            else:
                logger.error(f"API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching submissions: {e}")
            return None
    
    def get_solved_problems_by_topic(self, username: str) -> Optional[Dict[str, int]]:
        """Get solved problems categorized by topics"""
        query = """
        query skillStats($username: String!) {
            matchedUser(username: $username) {
                tagProblemCounts {
                    advanced {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                    intermediate {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                    fundamental {
                        tagName
                        tagSlug
                        problemsSolved
                    }
                }
            }
        }
        """
        
        try:
            response = requests.post(
                self.base_url,
                json={
                    "query": query,
                    "variables": {"username": username}
                },
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                matched_user = data.get("data", {}).get("matchedUser", {})
                tag_counts = matched_user.get("tagProblemCounts", {})
                
                # Aggregate all topics
                topics = {}
                for level in ["fundamental", "intermediate", "advanced"]:
                    for topic in tag_counts.get(level, []):
                        tag_name = topic.get("tagName")
                        solved = topic.get("problemsSolved", 0)
                        if tag_name and solved > 0:
                            topics[tag_name] = solved
                
                return topics
            else:
                logger.error(f"API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching topics: {e}")
            return None
    
    def get_calendar_data(self, username: str) -> Optional[Dict[str, Any]]:
        """Get submission calendar data"""
        try:
            stats = self.get_user_stats(username)
            if stats and stats.get("matchedUser"):
                calendar = stats["matchedUser"].get("userCalendar", {})
                submission_calendar = calendar.get("submissionCalendar")
                
                if submission_calendar:
                    # Parse the submission calendar JSON string
                    calendar_dict = json.loads(submission_calendar)
                    return {
                        "streak": calendar.get("streak", 0),
                        "totalActiveDays": calendar.get("totalActiveDays", 0),
                        "submissions": calendar_dict
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching calendar: {e}")
            return None
    
    def sync_user_data(self, username: str) -> Optional[Dict[str, Any]]:
        """Complete sync of user data from LeetCode"""
        logger.info(f"Starting LeetCode sync for user: {username}")
        
        try:
            # Fetch profile
            profile = self.get_user_profile(username)
            if not profile:
                return None
            
            # Fetch stats
            stats = self.get_user_stats(username)
            if not stats:
                return None
            
            # Fetch topics
            topics = self.get_solved_problems_by_topic(username)
            
            # Fetch calendar
            calendar = self.get_calendar_data(username)
            
            # Parse submission stats
            matched_user = stats.get("matchedUser", {})
            submit_stats = matched_user.get("submitStatsGlobal", {}).get("acSubmissionNum", [])
            
            total_solved = 0
            easy_solved = 0
            medium_solved = 0
            hard_solved = 0
            
            for stat in submit_stats:
                difficulty = stat.get("difficulty", "").upper()
                count = stat.get("count", 0)
                
                if difficulty == "ALL":
                    total_solved = count
                elif difficulty == "EASY":
                    easy_solved = count
                elif difficulty == "MEDIUM":
                    medium_solved = count
                elif difficulty == "HARD":
                    hard_solved = count
            
            sync_data = {
                "username": username,
                "totalSolved": total_solved,
                "easySolved": easy_solved,
                "mediumSolved": medium_solved,
                "hardSolved": hard_solved,
                "ranking": profile.get("profile", {}).get("ranking", 0),
                "streak": calendar.get("streak", 0) if calendar else 0,
                "totalActiveDays": calendar.get("totalActiveDays", 0) if calendar else 0,
                "topics": topics or {},
                "lastSynced": datetime.now().isoformat()
            }
            
            logger.info(f"Sync complete: {total_solved} problems solved")
            return sync_data
            
        except Exception as e:
            logger.error(f"Error during sync: {e}")
            return None


# Topic name mapping for learning paths
TOPIC_MAPPINGS = {
    "Arrays & Strings": ["Array", "String", "Hash Table"],
    "Dynamic Programming": ["Dynamic Programming"],
    "Trees & Graphs": ["Tree", "Binary Tree", "Graph", "Binary Search Tree", "Depth-First Search", "Breadth-First Search"],
    "System Design": ["Design", "System Design"]
}


def map_topics_to_learning_paths(topics: Dict[str, int]) -> Dict[str, int]:
    """Map LeetCode topics to learning path categories"""
    path_counts = {
        "Arrays & Strings": 0,
        "Dynamic Programming": 0,
        "Trees & Graphs": 0,
        "System Design": 0
    }
    
    for path_name, topic_list in TOPIC_MAPPINGS.items():
        for topic in topic_list:
            if topic in topics:
                path_counts[path_name] += topics[topic]
    
    return path_counts
