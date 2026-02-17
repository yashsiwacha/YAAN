import React, { useState, useEffect } from 'react';
import '../styles/CommandCenter.css';

interface LearningPath {
  id: number;
  title: string;
  category: string;
  totalProblems: number;
  completedProblems: number;
  progressPercent: number;
  color: string;
  icon: string;
}

interface Task {
  id: number;
  title: string;
  description?: string;
  priority: 'low' | 'medium' | 'high';
  completed: boolean;
  dueDate?: string;
}

interface ActivityDay {
  date: string;
  level: number;
  problemsSolved: number;
  timeSpent: number;
  streakDay: boolean;
}

interface Stats {
  current_streak: number;
  longest_streak: number;
  total_problems_solved: number;
  total_time_minutes: number;
}

interface LeetCodeSync {
  username: string;
  totalSolved: number;
  lastSynced: string;
}

const CommandCenter: React.FC = () => {
  const [learningPaths, setLearningPaths] = useState<LearningPath[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [heatmapData, setHeatmapData] = useState<ActivityDay[]>([]);
  const [stats, setStats] = useState<Stats>({
    current_streak: 0,
    longest_streak: 0,
    total_problems_solved: 0,
    total_time_minutes: 0
  });
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [showLeetCodeModal, setShowLeetCodeModal] = useState(false);
  const [leetcodeUsername, setLeetcodeUsername] = useState('');
  const [leetcodeStatus, setLeetcodeStatus] = useState<LeetCodeSync | null>(null);

  // Fetch all data on component mount
  useEffect(() => {
    fetchAllData();
    checkLeetCodeStatus();
  }, []);

  const checkLeetCodeStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/leetcode/status');
      const data = await response.json();
      if (data.success && data.data) {
        setLeetcodeStatus(data.data);
        setLeetcodeUsername(data.data.username);
      }
    } catch (error) {
      console.error('Error checking LeetCode status:', error);
    }
  };

  const syncLeetCode = async () => {
    if (!leetcodeUsername.trim()) {
      alert('Please enter your LeetCode username');
      return;
    }

    try {
      setSyncing(true);
      console.log('Syncing LeetCode account:', leetcodeUsername);

      const response = await fetch(`http://localhost:8000/api/leetcode/sync?username=${leetcodeUsername}`, {
        method: 'POST'
      });

      const data = await response.json();

      if (data.success) {
        console.log('LeetCode sync successful:', data.data);
        setLeetcodeStatus(data.data);
        setShowLeetCodeModal(false);
        
        // Refresh all data to show updated stats
        await fetchAllData();
        
        alert(`✅ Synced! ${data.data.totalSolved} problems solved`);
      } else {
        alert(`❌ Sync failed: ${data.error}`);
      }

      setSyncing(false);
    } catch (error) {
      console.error('Error syncing LeetCode:', error);
      alert('Failed to sync with LeetCode. Check your username and try again.');
      setSyncing(false);
    }
  };

  const handleRefreshClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    e.stopPropagation();
    console.log('Refresh button clicked!');
    fetchAllData();
  };

  const handleLeetCodeClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    e.stopPropagation();
    console.log('LeetCode button clicked!');
    setShowLeetCodeModal(true);
  };

  const fetchAllData = async () => {
    try {
      setLoading(true);
      console.log('Fetching data from backend...');
      
      const [pathsRes, tasksRes, activityRes, statsRes] = await Promise.all([
        fetch('http://localhost:8000/api/learning-paths'),
        fetch('http://localhost:8000/api/tasks'),
        fetch('http://localhost:8000/api/activity?days=90'),
        fetch('http://localhost:8000/api/stats')
      ]);

      console.log('API responses received');

      const pathsData = await pathsRes.json();
      const tasksData = await tasksRes.json();
      const activityData = await activityRes.json();
      const statsData = await statsRes.json();

      console.log('Learning paths:', pathsData.data?.length || 0);
      console.log('Tasks:', tasksData.data?.length || 0);
      console.log('Activity days:', activityData.data?.length || 0);
      console.log('Stats:', statsData.data);

      if (pathsData.success) setLearningPaths(pathsData.data);
      if (tasksData.success) setTasks(tasksData.data);
      if (activityData.success) setHeatmapData(activityData.data);
      if (statsData.success) setStats(statsData.data);

      setLoading(false);
      console.log('Data loaded successfully');
    } catch (error) {
      console.error('Error fetching data:', error);
      alert('Failed to connect to backend. Make sure the backend server is running on port 8000.');
      setLoading(false);
    }
  };

  const toggleTask = async (taskId: number, completed: boolean) => {
    try {
      const response = await fetch(`http://localhost:8000/api/tasks/${taskId}?completed=${!completed}`, {
        method: 'PUT'
      });
      const data = await response.json();
      if (data.success) {
        setTasks(tasks.map(task =>
          task.id === taskId ? { ...task, completed: !completed } : task
        ));
      }
    } catch (error) {
      console.error('Error toggling task:', error);
    }
  };

  const formatDueDate = (dueDate?: string) => {
    if (!dueDate) return 'No due date';
    const date = new Date(dueDate);
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    if (date.toDateString() === today.toDateString()) return 'Today';
    if (date.toDateString() === tomorrow.toDateString()) return 'Tomorrow';
    
    const diffDays = Math.ceil((date.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
    if (diffDays > 0 && diffDays <= 7) return `In ${diffDays} days`;
    
    return date.toLocaleDateString();
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  };

  const getLevelColor = (level: number) => {
    const colors = [
      'rgba(255, 255, 255, 0.05)',
      'rgba(99, 102, 241, 0.3)',
      'rgba(99, 102, 241, 0.5)',
      'rgba(99, 102, 241, 0.7)',
      'rgba(99, 102, 241, 0.9)'
    ];
    return colors[level];
  };

  if (loading) {
    return (
      <div className="command-center">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading Command Center...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="command-center">
      {/* Slim Sidebar */}
      <aside className="command-sidebar">
        <div className="neural-orb">
          <div className="orb-mini"></div>
        </div>
        <nav className="sidebar-nav">
          <button className="nav-icon active" title="Dashboard">
            🏠
          </button>
          <button className="nav-icon" title="Problems">
            💻
          </button>
          <button className="nav-icon" title="Analytics">
            📊
          </button>
          <button className="nav-icon" title="Sync">
            🔄
          </button>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="command-main">
        <header className="command-header">
          <div>
            <h1 className="command-title">Command Center</h1>
            <p className="command-subtitle">
              Track your coding journey
              {leetcodeStatus && (
                <span style={{ marginLeft: '16px', fontSize: '12px', color: '#10b981' }}>
                  🔗 Linked to LeetCode: @{leetcodeStatus.username}
                </span>
              )}
            </p>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <button 
              onClick={handleLeetCodeClick}
              disabled={syncing}
              style={{
                background: leetcodeStatus ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                border: leetcodeStatus ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid rgba(239, 68, 68, 0.3)',
                borderRadius: '8px',
                padding: '8px 16px',
                color: 'white',
                cursor: syncing ? 'wait' : 'pointer',
                fontSize: '14px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                opacity: syncing ? 0.6 : 1,
                pointerEvents: syncing ? 'none' : 'auto'
              }}
              title={leetcodeStatus ? 'Re-sync LeetCode' : 'Link LeetCode account'}
            >
              {syncing ? '⏳ Syncing...' : leetcodeStatus ? '🔄 Sync LeetCode' : '🔗 Link LeetCode'}
            </button>
            <button 
              onClick={handleRefreshClick}
              style={{
                background: 'rgba(99, 102, 241, 0.1)',
                border: '1px solid rgba(99, 102, 241, 0.3)',
                borderRadius: '8px',
                padding: '8px 16px',
                color: 'white',
                cursor: 'pointer',
                fontSize: '14px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                pointerEvents: 'auto'
              }}
              title="Refresh data"
            >
              🔄 Refresh
            </button>
            <div className="streak-badges">
              <div className="streak-badge">
                <span className="streak-icon">🔥</span>
                <div className="streak-info">
                  <span className="streak-value">{stats.current_streak}</span>
                  <span className="streak-label">Day Streak</span>
                </div>
              </div>
              <div className="streak-badge">
                <span className="streak-icon">⚡</span>
                <div className="streak-info">
                  <span className="streak-value">{stats.longest_streak}</span>
                  <span className="streak-label">Best Streak</span>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Learning Paths */}
        <section className="learning-paths">
          <h2 className="section-title">Learning Paths</h2>
          <div className="path-grid">
            {learningPaths.map(path => (
              <div key={path.id} className="path-card">
                <div className="path-header">
                  <span className="path-icon">{path.icon}</span>
                  <h3 className="path-title">{path.title}</h3>
                </div>
                <div className="path-progress">
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{ 
                        width: `${path.progressPercent}%`,
                        backgroundColor: path.color
                      }}
                    ></div>
                  </div>
                  <span className="progress-text">
                    {path.completedProblems}/{path.totalProblems} problems · {path.progressPercent}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Activity Heatmap */}
        <section className="activity-section">
          <h2 className="section-title">Activity</h2>
          <div className="heatmap-container">
            <div className="heatmap-grid">
              {heatmapData.map((day, idx) => (
                <div
                  key={idx}
                  className="heatmap-cell"
                  style={{ backgroundColor: getLevelColor(day.level) }}
                  title={`${day.date}: ${day.problemsSolved} problems`}
                ></div>
              ))}
            </div>
            <div className="heatmap-legend">
              <span>Less</span>
              {[0, 1, 2, 3, 4].map(level => (
                <div
                  key={level}
                  className="legend-cell"
                  style={{ backgroundColor: getLevelColor(level) }}
                ></div>
              ))}
              <span>More</span>
            </div>
          </div>
        </section>
      </main>

      {/* Right Panel - Tasks */}
      <aside className="command-tasks">
        <div className="tasks-header">
          <h2 className="tasks-title">Tasks & Reminders</h2>
          <button className="add-task-btn">+</button>
        </div>
        
        <div className="tasks-list">
          {tasks.map(task => (
            <div key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => toggleTask(task.id, task.completed)}
                className="task-checkbox"
              />
              <div className="task-content">
                <p className="task-title">{task.title}</p>
                {task.description && (
                  <p className="task-description">{task.description}</p>
                )}
                {task.dueDate && (
                  <span className="task-due">
                    Due: {formatDueDate(task.dueDate)}
                  </span>
                )}
              </div>
              <div 
                className="task-priority"
                style={{ backgroundColor: getPriorityColor(task.priority) }}
              ></div>
            </div>
          ))}
        </div>

        <div className="quick-stats">
          <div className="stat-item">
            <span className="stat-icon">✅</span>
            <div className="stat-info">
              <span className="stat-value">
                {tasks.filter(t => t.completed).length}/{tasks.length}
              </span>
              <span className="stat-label">Completed</span>
            </div>
          </div>
          <div className="stat-item">
            <span className="stat-icon">⏰</span>
            <div className="stat-info">
              <span className="stat-value">
                {tasks.filter(t => !t.completed && t.dueDate).length}
              </span>
              <span className="stat-label">Due Soon</span>
            </div>
          </div>
        </div>
      </aside>

      {/* LeetCode Sync Modal */}
      {showLeetCodeModal && (
        <div className="modal-overlay" onClick={() => !syncing && setShowLeetCodeModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>🔗 Link LeetCode Account</h2>
              <button 
                className="modal-close"
                onClick={() => setShowLeetCodeModal(false)}
                disabled={syncing}
              >
                ×
              </button>
            </div>
            
            <div className="modal-body">
              <p style={{ marginBottom: '16px', color: 'rgba(255, 255, 255, 0.7)' }}>
                Enter your LeetCode username to sync your problem-solving progress.
              </p>
              
              {leetcodeStatus && (
                <div style={{ 
                  background: 'rgba(16, 185, 129, 0.1)', 
                  border: '1px solid rgba(16, 185, 129, 0.3)',
                  borderRadius: '8px',
                  padding: '12px',
                  marginBottom: '16px'
                }}>
                  <div style={{ fontSize: '14px', color: '#10b981', marginBottom: '4px' }}>
                    ✅ Currently synced
                  </div>
                  <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.6)' }}>
                    {leetcodeStatus.totalSolved} problems solved • Last synced: {new Date(leetcodeStatus.lastSynced).toLocaleString()}
                  </div>
                </div>
              )}
              
              <input
                type="text"
                className="leetcode-username-input"
                placeholder="Enter LeetCode username"
                value={leetcodeUsername}
                onChange={(e) => setLeetcodeUsername(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && syncLeetCode()}
                disabled={syncing}
                autoFocus
              />
              
              <div style={{ 
                display: 'flex', 
                gap: '12px', 
                marginTop: '24px',
                justifyContent: 'flex-end'
              }}>
                <button
                  onClick={() => setShowLeetCodeModal(false)}
                  disabled={syncing}
                  style={{
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '8px',
                    padding: '10px 20px',
                    color: 'white',
                    cursor: syncing ? 'not-allowed' : 'pointer',
                    fontSize: '14px'
                  }}
                >
                  Cancel
                </button>
                <button
                  onClick={syncLeetCode}
                  disabled={syncing || !leetcodeUsername.trim()}
                  style={{
                    background: syncing || !leetcodeUsername.trim() ? 'rgba(99, 102, 241, 0.3)' : 'rgba(99, 102, 241, 0.8)',
                    border: '1px solid rgba(99, 102, 241, 0.5)',
                    borderRadius: '8px',
                    padding: '10px 20px',
                    color: 'white',
                    cursor: syncing || !leetcodeUsername.trim() ? 'not-allowed' : 'pointer',
                    fontSize: '14px',
                    fontWeight: 600
                  }}
                >
                  {syncing ? '⏳ Syncing...' : 'Sync Now'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CommandCenter;
