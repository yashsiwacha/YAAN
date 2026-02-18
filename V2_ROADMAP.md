# YAAN v2.0 - Detailed Roadmap

**Version:** 2.0.0  
**Status:** In Progress 🚧  
**Theme:** Advanced Code Intelligence & Community Features  
**Target Release:** May 1, 2026

---

## 🎯 Vision

Transform YAAN from a coding assistant into a comprehensive **AI-powered coding mentor** that helps developers:
- Solve algorithmic problems with intelligent code generation
- Learn through personalized paths and practice
- Collaborate with others on coding challenges
- Master data structures and algorithms with interactive guidance

---

## ✅ Progress Update (Feb 18, 2026)

### Recently Completed
- [x] Added backend auth foundation (password hashing, token sessions, register/login/logout/me)
- [x] Added DB schema + migration support for auth/session/LeetCode account linking
- [x] Implemented LeetCode credential login flow (username + password) with sync bootstrap
- [x] Wired desktop Command Center modal to both login modes:
    - YAAN username/password login
    - LeetCode username/password login
- [x] Fixed desktop interaction blocker (`pointer-events` overlay issue)
- [x] Improved Electron runtime resilience (backend UI fallback + Windows Python UTF-8 spawn env)

### Current Focus
- [ ] End-to-end UI acceptance validation for both login modes in packaged desktop flow
- [ ] Continue v2 LeetCode problems database and pattern-intelligence work

---

## 🚀 Major Features

### 1. LeetCode Problems Integration 🔥

**Priority:** HIGH | **Status:** 🚧 Core Auth/Sync In Progress

#### Overview
Build a comprehensive coding problems database with AI-powered solution generation. This feature will make YAAN an invaluable tool for interview preparation and algorithm learning.

#### Database Schema

```sql
-- Problems Table
CREATE TABLE problems (
    id INTEGER PRIMARY KEY,
    leetcode_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    difficulty TEXT CHECK(difficulty IN ('Easy', 'Medium', 'Hard')),
    acceptance_rate REAL,
    companies TEXT,  -- JSON array of companies
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Topics Table
CREATE TABLE topics (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

-- Problem Topics (Many-to-Many)
CREATE TABLE problem_topics (
    problem_id INTEGER,
    topic_id INTEGER,
    FOREIGN KEY (problem_id) REFERENCES problems(id),
    FOREIGN KEY (topic_id) REFERENCES topics(id),
    PRIMARY KEY (problem_id, topic_id)
);

-- Patterns Table
CREATE TABLE patterns (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    approach TEXT,  -- General approach description
    time_complexity TEXT,
    space_complexity TEXT
);

-- Problem Patterns
CREATE TABLE problem_patterns (
    problem_id INTEGER,
    pattern_id INTEGER,
    FOREIGN KEY (problem_id) REFERENCES problems(id),
    FOREIGN KEY (pattern_id) REFERENCES patterns(id),
    PRIMARY KEY (problem_id, pattern_id)
);

-- Solutions Table
CREATE TABLE solutions (
    id INTEGER PRIMARY KEY,
    problem_id INTEGER,
    language TEXT NOT NULL,
    code TEXT NOT NULL,
    explanation TEXT,
    approach_type TEXT,  -- 'brute_force', 'optimal', 'alternative'
    time_complexity TEXT,
    space_complexity TEXT,
    FOREIGN KEY (problem_id) REFERENCES problems(id)
);

-- User Progress
CREATE TABLE user_solutions (
    id INTEGER PRIMARY KEY,
    user_id TEXT,  -- For future multi-user support
    problem_id INTEGER,
    solved BOOLEAN DEFAULT FALSE,
    attempts INTEGER DEFAULT 0,
    last_attempted TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (problem_id) REFERENCES problems(id)
);
```

#### Core Topics (20+)

1. **Array** - Sorting, searching, manipulation
2. **String** - Pattern matching, manipulation
3. **Hash Table** - Fast lookups, frequency counting
4. **Dynamic Programming** - Optimization, memoization
5. **Math** - Number theory, calculations
6. **Binary Search** - Efficient searching
7. **Tree** - Binary tree, BST, traversals
8. **Depth-First Search** - Graph/tree exploration
9. **Breadth-First Search** - Level-order traversal
10. **Heap (Priority Queue)** - Top K problems
11. **Greedy** - Local optimal choices
12. **Backtracking** - Constraint satisfaction
13. **Graph** - Networks, paths, cycles
14. **Linked List** - Pointers, reversal
15. **Stack** - LIFO operations
16. **Queue** - FIFO operations
17. **Binary** - Bit manipulation
18. **Two Pointers** - Array/string problems
19. **Sliding Window** - Subarray problems
20. **Divide and Conquer** - Recursive splitting

#### Common Patterns (15+)

1. **Sliding Window** - Contiguous subarray problems
2. **Two Pointers** - Array manipulation, palindromes
3. **Fast & Slow Pointers** - Cycle detection
4. **Merge Intervals** - Overlapping ranges
5. **Cyclic Sort** - In-place array sorting
6. **In-place Reversal** - Linked list reversal
7. **Tree BFS** - Level-order traversal
8. **Tree DFS** - Inorder, preorder, postorder
9. **Top K Elements** - Heap-based selection
10. **K-way Merge** - Merging sorted arrays
11. **Binary Search** - Finding target in sorted data
12. **Backtracking** - Permutations, combinations
13. **Dynamic Programming** - Memoization, tabulation
14. **Greedy Algorithms** - Optimal local choices
15. **Graph Traversal (BFS/DFS)** - Connected components

#### Features Implementation

##### Phase 1: Database & Core (Week 1-2)
- [ ] Create database schema
- [ ] Import 100 easy problems
- [ ] Import 200 medium problems
- [ ] Import 200 hard problems
- [ ] Add topics and patterns
- [ ] Create data seeding scripts

##### Phase 2: Pattern Recognition (Week 3-4)
- [ ] Build pattern matching engine
- [ ] NLP intent for problem queries
- [ ] Keyword extraction (two sum, palindrome, etc.)
- [ ] Difficulty-based filtering
- [ ] Topic-based search
- [ ] Similar problems finder

##### Phase 3: Code Generation (Week 5-6)
- [ ] Template system for solutions
- [ ] Multi-language support (Python, Java, C++, JS)
- [ ] Approach explanation generator
- [ ] Complexity analysis display
- [ ] Multiple solution variants
- [ ] Step-by-step breakdown

##### Phase 4: Interactive Features (Week 7-8)
- [ ] Problem recommendation system
- [ ] Daily coding challenge
- [ ] Progress tracking dashboard
- [ ] "Solve next" suggestions
- [ ] Difficulty progression
- [ ] Learning path generator

#### New Intents

```python
"solve_problem": [
    r"solve (the )?(.+) problem",
    r"help me with (.+) problem",
    r"(show|generate) solution for (.+)",
    r"how to solve (.+)",
],

"find_problems": [
    r"find (.+) problems",
    r"show (easy|medium|hard) problems",
    r"problems about (.+)",
    r"(.+) (pattern|topic) problems",
],

"explain_approach": [
    r"explain (the )?(approach|solution) (for|to) (.+)",
    r"how does (.+) work",
    r"break down (.+) solution",
],

"daily_challenge": [
    r"daily (challenge|problem|question)",
    r"problem of the day",
    r"today'?s (challenge|problem)",
],

"recommend_problems": [
    r"recommend (me )?(a )?problem",
    r"suggest (a )?problem",
    r"what should i solve next",
    r"next problem",
],
```

#### User Interaction Examples

**Example 1: Direct Problem Request**
```
User: "solve two sum problem"
YAAN: 
## 📘 Problem: Two Sum
**Difficulty:** Easy | **Topics:** Array, Hash Table

### Problem Description
Given an array of integers nums and an integer target, return indices 
of the two numbers such that they add up to target.

### Pattern: Hash Table Lookup
**Approach:** Use a hash map to store complements

### Solution (Python)
[Shows optimal O(n) solution with explanation]

### Complexity
• Time: O(n)
• Space: O(n)

Would you like to see alternative approaches or try a similar problem?
```

**Example 2: Pattern-Based Search**
```
User: "show me sliding window problems"
YAAN:
## 🎯 Sliding Window Pattern Problems

**Easy (3):**
1. Maximum Average Subarray I
2. Minimum Size Subarray Sum
3. Longest Substring Without Repeating Characters

**Medium (5):**
4. Fruit Into Baskets
5. Longest Substring with K Distinct Characters
...

Which problem would you like to solve?
```

**Example 3: Daily Challenge**
```
User: "daily challenge"
YAAN:
## 🌟 Daily Challenge: February 17, 2026

**Problem:** Merge Intervals
**Difficulty:** Medium
**Topics:** Array, Sorting
**Companies:** Google, Facebook, Amazon

[Provides problem description and starts interactive solving]
```

---

### 2. Voice Mode Implementation 🎤

**Priority:** MEDIUM | **Status:** 📝 Design Phase

#### Features
- [ ] Wake word detection ("Hey YAAN")
- [ ] Continuous listening mode
- [ ] Voice command recognition
- [ ] Text-to-speech responses
- [ ] Voice speed control
- [ ] Multiple voice profiles
- [ ] Noise cancellation
- [ ] Offline voice recognition

#### Technical Stack
- Web Speech API (browser)
- Speech Recognition API
- Text-to-Speech API
- Web Audio API for processing

---

### 3. Advanced Learning System 🧠

**Priority:** MEDIUM | **Status:** 📝 Design Phase

#### Features
- [ ] Skill level assessment quiz
- [ ] Personalized learning paths
- [ ] Progress analytics dashboard
- [ ] Spaced repetition system
- [ ] Achievement badges
- [ ] Daily streaks
- [ ] Study session tracking
- [ ] Concept mastery levels

---

### 4. Collaboration Features 👥

**Priority:** LOW | **Status:** 📝 Design Phase

#### Features
- [x] User authentication (token session-based)
- [ ] Multi-user workspaces
- [ ] Shared problem solving
- [ ] Code review system
- [ ] Team challenges
- [ ] Leaderboards
- [ ] Group study sessions
- [ ] Mentorship matching

---

### 5. Multi-Device Sync 📱💻

**Priority:** MEDIUM | **Status:** 📝 Design Phase

#### Overview
Enable seamless synchronization of YAAN across multiple devices (phone, laptop, tablet) when connected to the same WiFi network. All conversation history, user preferences, reminders, and learning progress stay in sync in real-time.

#### Features
- [ ] Local network server discovery
- [ ] Real-time sync via WebSocket
- [ ] Cross-device conversation history
- [ ] Shared user profile & memory
- [ ] Synced reminders & todos
- [ ] Learning progress sync
- [ ] Conflict resolution strategy
- [ ] Optional authentication/PIN code
- [ ] Device management interface
- [ ] Sync status indicators
- [ ] Offline mode with sync on reconnect
- [ ] QR code pairing for easy device setup

#### Technical Implementation

**Server Configuration:**
```python
# Bind to all network interfaces instead of localhost
uvicorn.run(
    app, 
    host="0.0.0.0",  # Instead of 127.0.0.1
    port=8000
)
```

**Network Discovery:**
- mDNS/Bonjour for automatic device discovery
- Broadcast UDP packets for fallback
- Display server IP on UI for manual connection

**Database Sync:**
- SQLite databases already support this
- All devices connect to same server
- WebSocket ensures real-time updates
- No cloud services needed - pure local sync

**Security:**
```python
# Optional PIN/password protection
CREATE TABLE devices (
    id TEXT PRIMARY KEY,
    device_name TEXT NOT NULL,
    device_type TEXT,  -- 'mobile', 'desktop', 'tablet'
    last_seen TIMESTAMP,
    authorized BOOLEAN DEFAULT FALSE,
    pin_hash TEXT
);
```

**UI Enhancements:**
- Network indicator showing connected devices
- "Pair New Device" button with QR code
- Device list in settings
- "Disconnect All" option
- Sync status (syncing/synced/offline)

#### User Experience

**Desktop Setup:**
1. Start YAAN server
2. UI shows: "Server running at: http://192.168.1.100:8000"
3. QR code displayed for mobile pairing

**Mobile/Tablet Setup:**
1. Open YAAN web interface
2. Scan QR code OR enter IP address
3. Enter optional PIN if security enabled
4. Instant sync of all data

**Real-Time Sync:**
- Message sent on phone → instantly appears on laptop
- Reminder added on laptop → notification on all devices
- Memory learned on one device → available everywhere

#### Benefits
✅ Work across devices seamlessly  
✅ No cloud services - complete privacy  
✅ Real-time synchronization via existing WebSocket  
✅ Simple setup with QR code pairing  
✅ Optional security with PIN protection  
✅ Works on local WiFi - no internet required

#### Estimated Effort
**8-12 hours** for basic implementation, 15-20 hours with security & device management

---

## 🔧 Technical Improvements

### Performance
- [ ] Database indexing optimization
- [ ] Query caching (Redis)
- [ ] WebSocket connection pooling
- [ ] Response time <100ms for 95% queries
- [ ] Code minification & bundling
- [ ] Lazy loading for UI components

### Architecture
- [ ] Microservices consideration
- [ ] API versioning
- [ ] Rate limiting
- [ ] Request throttling
- [ ] Circuit breaker pattern
- [ ] Health check endpoints

### Testing
- [ ] Expand unit tests (95% coverage)
- [ ] Integration tests
- [ ] End-to-end tests (Playwright)
- [ ] Performance tests (load testing)
- [ ] Security testing
- [ ] Automated test pipeline

### DevOps
- [ ] GitHub Actions CI/CD
- [ ] Automated deployments
- [ ] Blue-green deployment
- [ ] Monitoring & alerting
- [ ] Log aggregation (ELK)
- [ ] APM integration

---

## 📅 Development Timeline (10 weeks)

### Phase 1: Planning & Design (Week 1)
- Finalize v2.0 specifications
- Design database schemas
- Create wireframes for new features
- Set up development environment

### Phase 2: LeetCode Integration (Week 2-5)
- Build problems database
- Implement pattern recognition
- Create code generation system
- Add new NLP intents
- Build recommendation engine

### Phase 3: Voice, Learning & Multi-Device (Week 6-7)
- Implement voice mode
- Build learning system
- Create progress tracking
- Add achievements
- **Implement multi-device sync**
- Network discovery & QR pairing
- Device management interface

### Phase 4: Polish & Testing (Week 8-9)
- UI/UX improvements
- Comprehensive testing
- Performance optimization
- Bug fixes

### Phase 5: Documentation & Release (Week 10)
- Update documentation
- Create demo videos
- Write blog posts
- Release v2.0.0

---

## 📊 Success Criteria

- ✅ 500+ problems in database
- ✅ <100ms response time (95th percentile)
- ✅ 90%+ intent matching accuracy
- ✅ Voice recognition 85%+ accuracy
- ✅ 95% test coverage
- ✅ Zero critical bugs
- ✅ 100+ active users in first month
- ✅ Positive user feedback (4.5+ stars)

---

## 🎯 Post-Release Plans (v2.1+)

- Mobile apps (React Native)
- VS Code extension
- Browser extensions
- GitHub integration
- Slack/Discord bots
- Plugin marketplace
- AI model integration (GPT-4, Claude)
- Enterprise features

---

**Status:** 🚧 Active Development  
**Next Steps:** Complete login-flow UI acceptance checks, then continue LeetCode problem pipeline (import + pattern mapping)  
**Questions?** Open a GitHub issue or discussion

**Let's build YAAN v2.0 together! 🚀**
