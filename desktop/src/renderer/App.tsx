import React, { useState, useRef, useEffect } from 'react';
import { io, Socket } from 'socket.io-client';
import ChatWindow from './components/ChatWindow';
import InputBar from './components/InputBar';
import Sidebar from './components/Sidebar';
import Settings from './components/Settings';
import Header from './components/Header';
import './styles/App.css';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [voiceMode, setVoiceMode] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const socketRef = useRef<Socket | null>(null);

  // Initialize WebSocket connection
  useEffect(() => {
    const backendUrl = (window as any).electronAPI?.getBackendUrl?.() || 'http://localhost:8000';
    
    socketRef.current = io(backendUrl, {
      transports: ['websocket'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    });

    socketRef.current.on('connect', () => {
      setIsConnected(true);
      console.log('✅ Connected to backend');
    });

    socketRef.current.on('disconnect', () => {
      setIsConnected(false);
      console.log('❌ Disconnected from backend');
    });

    socketRef.current.on('response', (data: { message: string }) => {
      const assistantMessage: Message = {
        id: Date.now().toString(),
        type: 'assistant',
        content: data.message,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);
      setIsLoading(false);
    });

    socketRef.current.on('error', (error: string) => {
      console.error('Socket error:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        type: 'assistant',
        content: `Error: ${error}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
      setIsLoading(false);
    });

    return () => {
      socketRef.current?.disconnect();
    };
  }, []);

  const handleSendMessage = (content: string) => {
    if (!content.trim() || !socketRef.current?.connected) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // Send via WebSocket
    socketRef.current.emit('message', {
      content,
      timestamp: new Date().toISOString()
    });
  };

  const handleClearChat = () => {
    setMessages([]);
  };

  const handleNewChat = () => {
    handleClearChat();
  };

  return (
    <div className="app">
      <Header 
        isConnected={isConnected}
        onMenuClick={() => setSidebarOpen(!sidebarOpen)}
        onSettingsClick={() => setShowSettings(true)}
        onVoiceToggle={() => setVoiceMode(!voiceMode)}
        voiceMode={voiceMode}
      />
      
      <div className="app-container">
        {sidebarOpen && (
          <Sidebar 
            onNewChat={handleNewChat}
            onClose={() => setSidebarOpen(false)}
          />
        )}
        
        <main className="main-content">
          {showSettings ? (
            <Settings onClose={() => setShowSettings(false)} />
          ) : (
            <>
              <ChatWindow 
                messages={messages}
                isLoading={isLoading}
              />
              <InputBar 
                onSendMessage={handleSendMessage}
                isLoading={isLoading}
                isConnected={isConnected}
                voiceMode={voiceMode}
              />
            </>
          )}
        </main>
      </div>
    </div>
  );
};

export default App;
