import React from 'react';
import '../styles/Sidebar.css';

interface SidebarProps {
  onNewChat: () => void;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ onNewChat, onClose }) => {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>YAAN</h2>
        <button className="close-btn" onClick={onClose}>✕</button>
      </div>

      <button className="new-chat-btn" onClick={onNewChat}>
        ➕ New Chat
      </button>

      <div className="sidebar-section">
        <h3>Recent Chats</h3>
        <ul className="chat-list">
          <li>Chat 1</li>
          <li>Chat 2</li>
          <li>Chat 3</li>
        </ul>
      </div>

      <div className="sidebar-section">
        <h3>Quick Access</h3>
        <ul className="quick-access-list">
          <li>📝 Notes</li>
          <li>📋 Reminders</li>
          <li>💡 Ideas</li>
          <li>🔍 Search</li>
        </ul>
      </div>

      <div className="sidebar-footer">
        <p>v2.0.0</p>
      </div>
    </aside>
  );
};

export default Sidebar;
