import React from 'react';
import '../styles/Header.css';
interface HeaderProps {
    isConnected: boolean;
    onMenuClick: () => void;
    onSettingsClick: () => void;
    onVoiceToggle: () => void;
    voiceMode: boolean;
}
declare const Header: React.FC<HeaderProps>;
export default Header;
