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
declare const Header: React.FC<HeaderProps>;
export default Header;
