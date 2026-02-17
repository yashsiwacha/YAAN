import React, { useEffect, useRef } from 'react';
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

const ChatWindow: React.FC<ChatWindowProps> = ({ messages, isLoading }) => {
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Auto-scroll to bottom when new messages arrive
    setTimeout(() => {
      endRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 0);
  }, [messages]);

  return (
    <div className="chat-area">
      {messages.length === 0 ? (
        <div className="message system">
          <div className="message-content">
            Welcome to YAAN - Your AI Assistant Network. How may I help you today?
          </div>
        </div>
      ) : (
        <>
          {messages.map((message) => (
            <div key={message.id} className={`message ${message.type}`}>
              <div className="message-content">{message.content}</div>
            </div>
          ))}
        </>
      )}
      <div ref={endRef} />
    </div>
  );
};

export default ChatWindow;
