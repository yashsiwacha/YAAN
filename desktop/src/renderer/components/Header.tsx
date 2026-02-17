import React from 'react';
import '../styles/Header.css';

interface HeaderProps {
  isConnected: boolean;
  onSettingsClick: () => void;
  onVoiceToggle: () => void;
  voiceMode: boolean;
  activeTab: 'chat' | 'voice';
  onTabChange: (tab: 'chat' | 'voice') => void;
}

const Header: React.FC<HeaderProps> = ({
  isConnected,
  onSettingsClick,
  onVoiceToggle,
  voiceMode,
  activeTab,
  onTabChange
}) => {
  return (
    <header className="header">
      <div className="header-left">
        <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
          <span className="status-dot"></span>
          <span className="status-text">
            {isConnected ? 'ONLINE' : 'OFFLINE'}
          </span>
        </div>
      </div>

      <div className="header-right">
        <button 
          className="icon-btn help-btn"
          title="Help"
        >
          ?
        </button>
        <button 
          className="icon-btn settings-btn"
          onClick={onSettingsClick}
          title="Settings"
        >
          ⚙
        </button>
        <button
          className={`tab-btn ${activeTab === 'voice' ? 'active' : ''}`}
          onClick={() => onTabChange('voice')}
        >
          VOICE
        </button>
        <button
          className={`tab-btn ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => onTabChange('chat')}
        >
          CHAT
        </button>
      </div>
    </header>
  );
};

export default Header;
