import React from 'react';
import '../styles/ChatWindow.css';
interface Message {
    id: string;
    type: 'user' | 'assistant' | 'system';
    content: string;
    timestamp: Date;
}
interface ChatWindowProps {
    messages: Message[];
    isLoading: boolean;
}
declare const ChatWindow: React.FC<ChatWindowProps>;
export default ChatWindow;
