import React, { useState } from 'react';
import '../styles/Settings.css';

interface SettingsProps {
  onClose: () => void;
}

const Settings: React.FC<SettingsProps> = ({ onClose }) => {
  const [theme, setTheme] = useState('dark');
  const [fontSize, setFontSize] = useState('medium');
  const [notifications, setNotifications] = useState(true);

  return (
    <div className="settings">
      <div className="settings-header">
        <h2>Settings</h2>
        <button className="close-btn" onClick={onClose}>✕</button>
      </div>

      <div className="settings-content">
        <div className="setting-group">
          <label>Theme</label>
          <select value={theme} onChange={(e) => setTheme(e.target.value)}>
            <option value="light">Light</option>
            <option value="dark">Dark</option>
            <option value="auto">Auto</option>
          </select>
        </div>

        <div className="setting-group">
          <label>Font Size</label>
          <select value={fontSize} onChange={(e) => setFontSize(e.target.value)}>
            <option value="small">Small</option>
            <option value="medium">Medium</option>
            <option value="large">Large</option>
          </select>
        </div>

        <div className="setting-group">
          <label>
            <input
              type="checkbox"
              checked={notifications}
              onChange={(e) => setNotifications(e.target.checked)}
            />
            Enable Notifications
          </label>
        </div>

        <div className="settings-section">
          <h3>About</h3>
          <p>YAAN Desktop v2.0.0</p>
          <p>AI-powered assistant for your desktop</p>
          <div className="settings-links">
            <a href="#">GitHub</a>
            <a href="#">Documentation</a>
            <a href="#">Report Issue</a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
