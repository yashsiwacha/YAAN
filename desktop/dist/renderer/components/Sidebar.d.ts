import React from 'react';
import '../styles/Sidebar.css';
interface SidebarProps {
    onNewChat: () => void;
    onClose: () => void;
}
declare const Sidebar: React.FC<SidebarProps>;
export default Sidebar;
