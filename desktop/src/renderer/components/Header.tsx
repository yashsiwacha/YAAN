import React from 'react';
import '../styles/Header.css';

interface HeaderProps {
  isConnected: boolean;
  onMenuClick: () => void;
  onSettingsClick: () => void;
  onVoiceToggle: () => void;
  voiceMode: boolean;
}

const Header: React.FC<HeaderProps> = ({
  isConnected,
  onMenuClick,
  onSettingsClick,
  onVoiceToggle,
  voiceMode
}) => {
  return (
    <header className="header">
      <div className="header-left">
        <button className="menu-btn" onClick={onMenuClick} title="Menu">
          ☰
        </button>
        <h1 className="app-title">YAAN</h1>
      </div>

      <div className="header-center">
        <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
          <span className="status-dot"></span>
          <span className="status-text">
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>

      <div className="header-right">
        <button
          className={`voice-btn ${voiceMode ? 'active' : ''}`}
          onClick={onVoiceToggle}
          title="Toggle Voice Mode"
        >
          🎤
        </button>
        <button 
          className="settings-btn"
          onClick={onSettingsClick}
          title="Settings"
        >
          ⚙️
        </button>
      </div>
    </header>
  );
};

export default Header;
